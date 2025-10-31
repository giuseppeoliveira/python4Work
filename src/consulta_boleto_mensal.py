import os
import re
import time
import json
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
    if not isinstance(cpf_raw, str):
        cpf_raw = str(cpf_raw)
    cpf_limpo = re.sub(r"\D", "", cpf_raw)
    return cpf_limpo.zfill(11) if cpf_limpo else ""


def _request_divida_xml(cpf: str, session: requests.Session, timeout: int = 10) -> str:
    """Faz POST na API ObterDividaAtivaPorCPF e retorna o XML decodificado (string).
    Em caso de falha retorna empty string.
    """
    payload = {"logonUsuario": LOGIN, "senhaUsuario": SENHA, "cpfCnpj": cpf}
    try:
        resp = session.post(URL_DIVIDA, data=payload, timeout=timeout)
        resp.raise_for_status()
        text = resp.text
        # decodifica entities comuns
        decoded = text.replace("&lt;", "<").replace("&gt;", ">")
        return decoded
    except Exception as e:
        # retornar string vazia para sinalizar erro
        return ""


def _extract_divida_blocks_from_xml(xml_text: str):
    """Extrai blocos <DividaAtiva> como BeautifulSoup Tag list"""
    if not xml_text:
        return []
    try:
        soup = BeautifulSoup(xml_text, "xml")
        blocks = soup.find_all("DividaAtiva")
        return blocks
    except Exception:
        return []


def _block_to_dict(block):
    """Converte um bloco BeautifulSoup <DividaAtiva> em dict simples dos campos filhos"""
    data = {}
    try:
        for child in block.find_all(recursive=False):
            key = child.name
            val = child.text.strip() if child.text else ""
            data[key] = val
    except Exception:
        pass
    return data


def processar_cpf_obter_blocos(cpf_raw: str, year: int, month: int, session: requests.Session = None):
    cpf = limpar_cpf(cpf_raw)
    if not cpf:
        return []
    own_session = False
    if session is None:
        session = requests.Session()
        own_session = True
    try:
        xml = _request_divida_xml(cpf, session)
        blocks = _extract_divida_blocks_from_xml(xml)
        prefix = f"{year:04d}-{month:02d}"
        resultado = []
        for b in blocks:
            d = _block_to_dict(b)
            # Procurar campo DataVencimento no d (chave pode existir ou não)
            dv = d.get("DataVencimento", "")
            if dv.startswith(prefix):
                d["cpf"] = cpf
                resultado.append(d)
        return resultado
    finally:
        if own_session:
            session.close()


def run_consulta_boleto(caminho_entrada: str, caminho_saida: str, year: int, month: int, max_workers: int = 12):
    """Processa o arquivo de entrada e grava um Excel com todos os blocos filtrados.

    Entrada: Excel com colunas `cod_aluno` e `cpf` (case-insensitive)
    Saída: Excel com uma linha por bloco DividaAtiva filtrado, contendo os campos do bloco + cpf + cod_aluno
    """
    if not LOGIN or not SENHA:
        raise RuntimeError("Variáveis de ambiente LOGIN e SENHA não configuradas (arquivo .env)")

    df = pd.read_excel(caminho_entrada, engine="openpyxl", dtype=str)
    # Normalizar colunas
    df.columns = df.columns.str.strip().str.lower()
    # Tentar encontrar colunas
    if "cpf" not in df.columns:
        raise ValueError("Arquivo de entrada deve conter coluna 'cpf'")

    # Se tiver cod_aluno, manter, senão adicionar vazio
    cod_aluno_col = None
    for c in ["cod_aluno", "codaluno", "matricula"]:
        if c in df.columns:
            cod_aluno_col = c
            break
    if cod_aluno_col is None:
        df["cod_aluno"] = ""
        cod_aluno_col = "cod_aluno"

    session = requests.Session()

    resultados = []
    rows = df.to_dict(orient="records")

    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(processar_cpf_obter_blocos, row.get("cpf", ""), year, month, session): row for row in rows}
        for future in as_completed(futures):
            row = futures[future]
            try:
                blocos = future.result()
                for b in blocos:
                    # anexar cod_aluno e cpf original
                    b["cod_aluno"] = row.get(cod_aluno_col, "")
                    b["cpf_original"] = row.get("cpf", "")
                    resultados.append(b)
            except Exception as e:
                # registro de erro mínimo
                continue

    session.close()

    if resultados:
        out_df = pd.DataFrame(resultados)
    else:
        out_df = pd.DataFrame(columns=["cpf", "cod_aluno", "DataVencimento"])  # vazio com colunas mínimas

    out_df.to_excel(caminho_saida, index=False)
    return caminho_saida


if __name__ == "__main__":
    # Execução rápida para debug
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int)
    args = parser.parse_args()
    print("Rodando consulta boleto mensal...")
    run_consulta_boleto(args.input, args.output, args.year, args.month)
