import pandas as pd
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import time
import re
import unicodedata
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

LOGIN_FIXO = os.getenv("LOGIN")
SENHA_FIXO = os.getenv("SENHA")
URL_DIVIDA = os.getenv("URL_DIVIDA", "http://54.83.29.48/easycollectorws/easycollectorWs.asmx/ObterDividaAtivaPorCPF")

# Verifica se as variáveis de ambiente foram carregadas
if not all([LOGIN_FIXO, SENHA_FIXO]):
    raise ValueError("❌ Erro: Variáveis de ambiente LOGIN e SENHA não encontradas. Verifique o arquivo .env")

parar_evento = threading.Event()
cancelar_evento = threading.Event()

# Sessão HTTP reutilizável para melhor performance
session = requests.Session()
session.headers.update({'Connection': 'keep-alive'})

def remover_acentos(texto):
    """
    Remove acentos de uma string.
    """
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")

def limpar_cpf(cpf_raw):
    if not isinstance(cpf_raw, str):
        cpf_raw = str(cpf_raw)
    cpf_limpo = re.sub(r'\D', '', cpf_raw)
    return cpf_limpo.zfill(11) if cpf_limpo else ""

def consultar_easycollector(cpf, login, senha):
    payload = {
        "logonUsuario": login,
        "senhaUsuario": senha,
        "cpfCnpj": cpf
    }
    try:
        # Reduzido timeout de 10s para 5s para melhor performance
        response = session.post(URL_DIVIDA, data=payload, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "xml")
        body_text = soup.get_text()

        id_cliente_vals = [
            int(val.split("</IdCliente>")[0].strip())
            for val in body_text.split("<IdCliente>")[1:]
            if val.split("</IdCliente>")[0].strip().isdigit()
        ]
        id_acordo_vals = [
            int(val.split("</IdAcordo>")[0].strip())
            for val in body_text.split("<IdAcordo>")[1:]
            if val.split("</IdAcordo>")[0].strip().isdigit()
        ]
        data_vencs = [
            val.split("</DataVencimento>")[0].strip()
            for val in body_text.split("<DataVencimento>")[1:]
        ]

        id_cliente = next((v for v in reversed(id_cliente_vals) if v != 0), 0)
        id_acordo = next((v for v in reversed(id_acordo_vals) if v != 0), 0)

        return id_cliente, id_acordo, data_vencs

    except Exception as e:
        print(f"❌ [ERRO] CPF {cpf}: {e}")
        return 0, 0, []

def processar_linha_cpf(row_data):
    """Processa uma única linha de CPF"""
    i, row = row_data
    
    cod_acordo = row.get("cod_acordo", "0")
    cod_cliente = row.get("cod_cliente", "0")

    if cod_acordo != "0" or cod_cliente != "0":
        # Já possui os códigos → marcar como Excluir
        return i, "Excluir", "Em Duplicidade", cod_cliente, cod_acordo

    # Para registros com cod_acordo e cod_cliente igual a 0, tenta atualizar
    cpf_raw = row.get("cpf", "")
    cpf = limpar_cpf(cpf_raw)

    if not cpf or cpf == "00000000000":
        return i, "", "", "0", "0"

    id_cliente, id_acordo, datas = consultar_easycollector(cpf, LOGIN_FIXO, SENHA_FIXO)

    alterou = False
    new_cod_cliente = cod_cliente
    new_cod_acordo = cod_acordo

    if id_cliente != 0:
        new_cod_cliente = str(id_cliente)
        alterou = True

    if id_acordo != 0:
        new_cod_acordo = str(id_acordo)
        alterou = True

    if alterou and (new_cod_cliente != "0" or new_cod_acordo != "0"):
        status = "Update"
        observacao = "Atualizado"
    elif id_cliente == 0 and id_acordo == 0:
        # Só marca como "Não Encontrado" se a API não retornou NENHUM dado
        status = "Investigar"
        observacao = "Não Encontrado"
    else:
        status = ""
        observacao = ""

    print(f"[Linha {i+1}] CPF: {cpf} | cod_cliente: {id_cliente} | cod_acordo: {id_acordo} | status: {status}")
    
    return i, status, observacao, new_cod_cliente, new_cod_acordo

def processar_batch_cpf(batch_rows):
    """Processa um lote de CPFs em paralelo"""
    results = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_row = {
            executor.submit(processar_linha_cpf, row_data): row_data 
            for row_data in batch_rows
        }
        
        for future in as_completed(future_to_row):
            row_data = future_to_row[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                i, row = row_data
                print(f"Erro no processamento da linha {i}: {e}")
                results.append((i, "Erro", f"Erro: {str(e)}", "0", "0"))
    
    return results

def processar_xlsx(caminho_arquivo, caminho_salvar, progresso_var, progresso_label, status_label):
    try:
        df = pd.read_excel(caminho_arquivo, engine='openpyxl', dtype=str)
        # Limpar nomes das colunas: remover espaços, deixar minúsculas e retirar acentos
        df.columns = df.columns.str.strip().str.lower().map(remover_acentos)
        print(f"[INFO] Colunas detectadas no XLSX: {df.columns.tolist()}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler XLSX:\n{e}")
        return

    if "cpf" not in df.columns or "status" not in df.columns or "observacao" not in df.columns:
        messagebox.showerror("Erro", "O arquivo deve conter as colunas 'cpf', 'status' e 'observacao'.")
        return

    df.fillna("0", inplace=True)

    total = len(df)
    tempo_inicio = time.time()
    batch_size = 25  # Processa 25 linhas por vez
    linhas_processadas = 0

    # Processar em lotes para melhor performance
    for batch_start in range(0, total, batch_size):
        if cancelar_evento.is_set():
            status_label.config(text="Processo cancelado. Nenhuma alteração salva.")
            print("[INFO] Processo cancelado pelo usuário. Nenhuma alteração salva.")
            return
        if parar_evento.is_set():
            status_label.config(text=f"Processo parado. Salvando progresso até linha {batch_start}...")
            print(f"[INFO] Processo parado pelo usuário. Salvando progresso até linha {batch_start}...")
            df.iloc[:batch_start].to_excel(caminho_salvar, index=False, engine='openpyxl')
            progresso_var.set(100)
            progresso_label.config(text="100%")
            messagebox.showinfo("Interrompido", f"Progresso salvo até a linha {batch_start} em:\n{caminho_salvar}")
            return

        batch_end = min(batch_start + batch_size, total)
        batch_rows = [(i, df.iloc[i]) for i in range(batch_start, batch_end)]
        
        # Processar lote em paralelo
        batch_results = processar_batch_cpf(batch_rows)
        
        # Atualizar DataFrame com resultados
        for i, status, observacao, cod_cliente, cod_acordo in batch_results:
            df.at[i, "status"] = status
            df.at[i, "observacao"] = observacao
            df.at[i, "cod_cliente"] = cod_cliente
            df.at[i, "cod_acordo"] = cod_acordo
            linhas_processadas += 1

        # Atualizar progresso
        progresso = int((linhas_processadas / total) * 100)
        progresso_var.set(progresso)
        progresso_label.config(text=f"{progresso}%")

        # Calcular tempo estimado
        tempo_passado = time.time() - tempo_inicio
        if linhas_processadas > 0:
            tempo_estimado_restante = (tempo_passado / linhas_processadas) * (total - linhas_processadas)
            minutos = int(tempo_estimado_restante // 60)
            segundos = int(tempo_estimado_restante % 60)
            status_label.config(text=f"Processando: {linhas_processadas}/{total} - Tempo estimado restante: {minutos}m {segundos}s")
        
        # Salvar progresso a cada 100 linhas processadas
        if linhas_processadas % 100 == 0:
            df.to_excel(caminho_salvar, index=False, engine='openpyxl')

    # Salvar arquivo final
    df.to_excel(caminho_salvar, index=False, engine='openpyxl')
    progresso_var.set(100)
    progresso_label.config(text="100%")
    status_label.config(text=f"Arquivo salvo: {caminho_salvar}")
    print(f"[INFO] Processamento finalizado. Arquivo salvo em {caminho_salvar}")
    messagebox.showinfo("Finalizado", f"Processamento concluído.\nArquivo salvo como:\n{caminho_salvar}")

def iniciar_processo(caminho_arquivo, caminho_salvar, progresso_var, progresso_label, status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    botao_iniciar.config(state="disabled")
    botao_cancelar.config(state="normal")
    botao_parar.config(state="normal")
    botao_arquivo.config(state="disabled")

    parar_evento.clear()
    cancelar_evento.clear()

    thread = threading.Thread(
        target=processar_xlsx,
        args=(caminho_arquivo, caminho_salvar, progresso_var, progresso_label, status_label)
    )
    thread.start()

def cancelar_processo(status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    cancelar_evento.set()
    parar_evento.set()
    status_label.config(text="Cancelando processo...")
    print("[INFO] Usuário solicitou cancelar o processo.")
    botao_iniciar.config(state="normal")
    botao_cancelar.config(state="disabled")
    botao_parar.config(state="disabled")
    botao_arquivo.config(state="normal")

def parar_processo(status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    parar_evento.set()
    status_label.config(text="Parando processo... Salvando progresso...")
    print("[INFO] Usuário solicitou parar o processo para salvar progresso parcial.")
    botao_iniciar.config(state="normal")
    botao_cancelar.config(state="disabled")
    botao_parar.config(state="disabled")
    botao_arquivo.config(state="normal")

def escolher_arquivo(progresso_var, progresso_label, status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo XLSX",
        filetypes=[("Excel Files", "*.xlsx")]
    )
    if not caminho_arquivo:
        status_label.config(text="Nenhum arquivo selecionado.")
        return None, None

    caminho_salvar = filedialog.asksaveasfilename(
        title="Escolha onde salvar o arquivo atualizado",
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        initialfile="arquivo_atualizado.xlsx"
    )
    if not caminho_salvar:
        status_label.config(text="Local para salvar não selecionado.")
        return None, None

    progresso_var.set(0)
    progresso_label.config(text="0%")
    status_label.config(text="Arquivo selecionado. Pronto para iniciar.")
    botao_iniciar.config(state="normal")
    botao_cancelar.config(state="disabled")
    botao_parar.config(state="disabled")

    return caminho_arquivo, caminho_salvar

# --- Interface Gráfica ---
def main():
    root = tk.Tk()
    root.title("Obter Divida por CPF - Etapa 1")
    root.geometry("600x200")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    progresso_var = tk.IntVar()

    progresso_bar = ttk.Progressbar(frame, variable=progresso_var, maximum=100, length=500)
    progresso_bar.pack(pady=5)

    progresso_label = ttk.Label(frame, text="0%")
    progresso_label.pack()

    status_label = ttk.Label(frame, text="Nenhum arquivo selecionado.")
    status_label.pack(pady=5)

    botao_arquivo = ttk.Button(frame, text="Escolher Arquivo")
    botao_arquivo.pack(side="left", padx=5)

    botao_iniciar = ttk.Button(frame, text="Obter Divida por CPF", state="disabled")
    botao_iniciar.pack(side="left", padx=5)

    botao_parar = ttk.Button(frame, text="Parar (Salvar progresso)", state="disabled")
    botao_parar.pack(side="left", padx=5)

    botao_cancelar = ttk.Button(frame, text="Cancelar (Não salvar)", state="disabled")
    botao_cancelar.pack(side="left", padx=5)

    caminho_arquivo = None
    caminho_salvar = None

    def on_escolher_arquivo():
        nonlocal caminho_arquivo, caminho_salvar
        caminho_arquivo, caminho_salvar = escolher_arquivo(
            progresso_var, progresso_label, status_label,
            botao_iniciar, botao_cancelar, botao_parar, botao_arquivo
        )

    def on_iniciar():
        if not caminho_arquivo or not caminho_salvar:
            messagebox.showwarning("Atenção", "Escolha o arquivo e onde salvar antes de iniciar.")
            return
        iniciar_processo(
            caminho_arquivo, caminho_salvar,
            progresso_var, progresso_label, status_label,
            botao_iniciar, botao_cancelar, botao_parar, botao_arquivo
        )

    def on_parar():
        parar_processo(status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo)

    def on_cancelar():
        cancelar_processo(status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo)

    botao_arquivo.config(command=on_escolher_arquivo)
    botao_iniciar.config(command=on_iniciar)
    botao_parar.config(command=on_parar)
    botao_cancelar.config(command=on_cancelar)

    root.mainloop()

if __name__ == "__main__":
    main()
