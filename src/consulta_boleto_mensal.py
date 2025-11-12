import os
import re
import time
from typing import List, Tuple

import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

URL_DIVIDA = os.getenv("URL_DIVIDA", "http://54.83.29.48/easycollectorws/easycollectorWs.asmx/ObterDividaAtivaPorCPF")
LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")


def limpar_cpf(cpf_raw: str) -> str:
    if cpf_raw is None:
        return ""
    if not isinstance(cpf_raw, str):
        cpf_raw = str(cpf_raw)
    cpf_limpo = re.sub(r"\D", "", cpf_raw)
    return cpf_limpo.zfill(11) if cpf_limpo else ""


def _request_divida_xml(cpf: str, login: str, senha: str, session: requests.Session, timeout: int = 12) -> str:
    payload = {"logonUsuario": login, "senhaUsuario": senha, "cpfCnpj": cpf}
    try:
        resp = session.post(URL_DIVIDA, data=payload, timeout=timeout)
        resp.raise_for_status()
        text = resp.text
        decoded = text.replace("&lt;", "<").replace("&gt;", ">")
        return decoded
    except Exception:
        return ""


def _extract_divida_blocks_from_xml(xml_text: str):
    if not xml_text:
        return []
    try:
        soup = BeautifulSoup(xml_text, "xml")
        blocks = soup.find_all("DividaAtiva")
        return blocks
    except Exception:
        return []


def _block_to_dict(block) -> dict:
    d = {}
    try:
        for child in block.find_all(recursive=False):
            d[child.name] = child.text.strip() if child.text else ""
    except Exception:
        pass
    return d


def _parse_periods(period_lines: List[str]) -> List[str]:
    """Converte linhas de entrada em prefixos YYYY-MM válidos."""
    prefixes = []
    for line in period_lines:
        s = str(line).strip()
        if not s:
            continue
        # aceitar formatos como YYYY-MM ou YYYYMM
        if re.match(r"^\d{4}-\d{2}$", s):
            prefixes.append(s)
            continue
        if re.match(r"^\d{6}$", s):
            prefixes.append(f"{s[:4]}-{s[4:6]}")
            continue
        # tentar extrair ano e mês de strings como '2025/08' ou '08-2025'
        m = re.search(r"(\d{4}).*?(\d{1,2})", s)
        if m:
            year = m.group(1)
            month = int(m.group(2))
            if 1 <= month <= 12:
                prefixes.append(f"{year}-{month:02d}")
    # remover duplicatas mantendo ordem
    seen = set()
    out = []
    for p in prefixes:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def run_consulta_boleto_from_rows(rows: List[Tuple[str, str]], caminho_saida: str, periods: List[str], login: str = None, senha: str = None, max_workers: int = 12):
    """Processa uma lista de tuples (cod_aluno, cpf_raw) e grava um Excel com os blocos que batem em qualquer period (YYYY-MM).

    rows: list of (cod_aluno, cpf_raw)
    periods: list of prefix strings like '2025-08'
    """
    if login is None or senha is None:
        login = LOGIN
        senha = SENHA
    if not login or not senha:
        raise RuntimeError("Credenciais LOGIN/SENHA não fornecidas")

    prefixes = set(periods)

    session = requests.Session()

    results = []

    def worker(item):
        cod_aluno, cpf_raw = item
        cpf = limpar_cpf(cpf_raw)
        if not cpf:
            return [{'cod_aluno': cod_aluno, 'cpf': cpf_raw, 'status': 'CPF inválido'}]
        xml = _request_divida_xml(cpf, login, senha, session)
        blocks = _extract_divida_blocks_from_xml(xml)
        if not blocks:
            return [{'cod_aluno': cod_aluno, 'cpf': cpf, 'status': 'Erro ao consultar ou sem resposta'}]
        matched = []
        for b in blocks:
            d = _block_to_dict(b)
            dv = d.get('DataVencimento', '') or d.get('Data_Vencimento', '') or d.get('dataVencimento', '')
            for p in prefixes:
                if dv.startswith(p):
                    # adicionar informação do período que bateu
                    rec = dict(d)
                    rec['cod_aluno'] = cod_aluno
                    rec['cpf'] = cpf
                    rec['period'] = p
                    matched.append(rec)
                    break
        if not matched:
            return [{'cod_aluno': cod_aluno, 'cpf': cpf, 'status': 'Nenhuma dívida encontrada para os períodos selecionados'}]
        return matched

    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(worker, r): r for r in rows}
        for future in as_completed(futures):
            try:
                res = future.result()
                results.extend(res)
            except Exception as e:
                results.append({'cod_aluno': '', 'cpf': '', 'status': f'Erro interno: {e}'})

    session.close()

    df_out = pd.DataFrame(results)
    # garantir colunas consistentes
    if 'period' not in df_out.columns:
        df_out['period'] = ''
    df_out.to_excel(caminho_saida, index=False, engine='openpyxl')
    return caminho_saida


def run_consulta_boleto(caminho_entrada: str, caminho_saida: str, period_lines: List[str], login: str = None, senha: str = None, max_workers: int = 12):
    """Lê um arquivo Excel com colunas cod_aluno e cpf e processa para os períodos informados (lista de strings)."""
    prefixes = _parse_periods(period_lines)
    if not prefixes:
        raise ValueError("Nenhum período válido informado (ex: 2025-08).")

    df = pd.read_excel(caminho_entrada, engine='openpyxl', dtype=str)
    df.columns = df.columns.str.strip().str.lower()
    if 'cpf' not in df.columns:
        raise ValueError("Arquivo de entrada deve conter a coluna 'cpf'")
    # encontrar coluna cod_aluno
    cod_col = None
    for c in ['cod_aluno', 'codaluno', 'matricula']:
        if c in df.columns:
            cod_col = c
            break
    if cod_col is None:
        df['cod_aluno'] = ''
        cod_col = 'cod_aluno'

    rows = [(r.get(cod_col, ''), r.get('cpf', '')) for r in df.to_dict(orient='records')]
    return run_consulta_boleto_from_rows(rows, caminho_saida, prefixes, login, senha, max_workers)


if __name__ == '__main__':
    print('Uso: importar e chamar run_consulta_boleto(...) ou run_consulta_boleto_from_rows(...)')
