import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import threading
import time
import os
import re
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")
URL = os.getenv("URL")

# Verifica se as variáveis de ambiente foram carregadas
if not all([LOGIN, SENHA, URL]):
    raise ValueError("❌ Erro: Variáveis de ambiente não encontradas. Verifique o arquivo .env")

parar_flag = threading.Event()
linhas_processadas = 0
total_erros = 0
log_erros = []

# Sessão HTTP reutilizável para melhor performance
session = requests.Session()
session.headers.update({'Connection': 'keep-alive'})

def consultar_status_acordo(row, index, tentativas=2):
    global total_erros
    cod_cliente = row.get("cod_cliente", 0)
    cod_acordo = row.get("cod_acordo", 0)

    payload = {
        "logonUsuario": LOGIN,
        "senhaUsuario": SENHA,
        "idCliente": int(cod_cliente),
        "idAcordo": int(cod_acordo)
    }

    for tentativa in range(1, tentativas + 1):
        try:
            # Reduzido timeout de 15s para 5s
            response = session.post(URL, data=payload, timeout=5)
            response.raise_for_status()

            # Parse XML mais eficiente
            soup = BeautifulSoup(response.content, "xml")
            string_tag = soup.find("string")

            if not string_tag:
                raise ValueError("⚠️ Tag <string> não encontrada.")

            decoded = string_tag.text.replace("&lt;", "<").replace("&gt;", ">")
            
            # Regex mais eficiente com compilação
            status_match = re.search(r"<Status>(.*?)</Status>", decoded)

            if status_match:
                return status_match.group(1)
            else:
                raise ValueError("⚠️ Campo <Status> não encontrado.")

        except requests.exceptions.Timeout:
            log = f"Linha {index + 1}: ⏰ Timeout na tentativa {tentativa} - cod_cliente={cod_cliente}, cod_acordo={cod_acordo}"
        except requests.exceptions.RequestException as e:
            log = f"Linha {index + 1}: ❌ Erro HTTP {e.__class__.__name__}: {str(e)} - cod_cliente={cod_cliente}, cod_acordo={cod_acordo}"
        except Exception as e:
            log = f"Linha {index + 1}: ❌ Erro inesperado: {e}"

        log_erros.append(log)
        print(log)

    total_erros += 1
    return "Não encontrado"

def consultar_status_acordo_batch(rows_batch):
    """Processa um lote de consultas em paralelo"""
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_row = {
            executor.submit(consultar_status_acordo, row, index): (index, row) 
            for index, row in rows_batch
        }
        
        for future in as_completed(future_to_row):
            index, row = future_to_row[future]
            try:
                status = future.result()
                results.append((index, status))
            except Exception as e:
                print(f"Erro no processamento da linha {index}: {e}")
                results.append((index, "Erro"))
    
    return results

def salvar_parcial(df, caminho_salvar, force=False):
    """Salva o arquivo apenas a cada X linhas ou quando forçado"""
    try:
        if force or linhas_processadas % 50 == 0:  # Salva a cada 50 linhas
            df.to_excel(caminho_salvar, index=False)
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

def escolher_arquivo(progresso_var, progresso_label, status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if caminho:
        salvar_em = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
        if salvar_em:
            status_label.config(text=f"Arquivo selecionado: {os.path.basename(caminho)}")
            botao_iniciar.config(state="normal")
            botao_cancelar.config(state="normal")
            botao_parar.config(state="normal")
            botao_arquivo.config(state="disabled")
            return caminho, salvar_em
    return None, None

def iniciar_processo(caminho_arquivo, caminho_salvar, progresso_var, progresso_label, status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    parar_flag.clear()
    threading.Thread(target=processar_arquivo, args=(caminho_arquivo, caminho_salvar, progresso_var, progresso_label, status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo)).start()

def processar_arquivo(caminho_arquivo, caminho_salvar, progresso_var, progresso_label, status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    global linhas_processadas, log_erros, total_erros
    df = pd.read_excel(caminho_arquivo)
    if 'status_acordo' not in df.columns:
        df["status_acordo"] = ""
    linhas_processadas = 0
    total = len(df)
    batch_size = 20  # Processa 20 linhas por vez

    start_time = time.time()

    # Processar em lotes para melhor performance
    for batch_start in range(0, total, batch_size):
        if parar_flag.is_set():
            break
            
        batch_end = min(batch_start + batch_size, total)
        batch_rows = [(i, df.iloc[i]) for i in range(batch_start, batch_end)]
        
        # Processar lote em paralelo
        batch_results = consultar_status_acordo_batch(batch_rows)
        
        # Atualizar DataFrame com resultados
        for index, status in batch_results:
            df.at[index, "status_acordo"] = status
            linhas_processadas += 1

        # Atualizar progresso
        progresso = int((linhas_processadas / total) * 100)
        progresso_var.set(progresso)
        progresso_label.config(text=f"{linhas_processadas}/{total}")
        
        # Calcular tempo estimado
        elapsed_time = time.time() - start_time
        if linhas_processadas > 0:
            avg_time_per_item = elapsed_time / linhas_processadas
            remaining_items = total - linhas_processadas
            estimated_remaining = avg_time_per_item * remaining_items
            minutes = int(estimated_remaining // 60)
            seconds = int(estimated_remaining % 60)
            status_label.config(text=f"Processando: {linhas_processadas}/{total} - Restam ~{minutes}m {seconds}s")
        
        # Salvar progresso periodicamente
        salvar_parcial(df, caminho_salvar)

    # Salvar arquivo final
    salvar_parcial(df, caminho_salvar, force=True)

    # Salvar log de erros
    with open("log_consultar_acordo.txt", "w", encoding="utf-8") as f:
        for linha in log_erros:
            f.write(linha + "\n")

    status_label.config(text="✅ Processamento finalizado.")
    botao_iniciar.config(state="disabled")
    botao_parar.config(state="disabled")
    botao_cancelar.config(state="disabled")
    botao_arquivo.config(state="normal")

def parar_processo(status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    parar_flag.set()
    status_label.config(text="⏹️ Processamento interrompido.")
    botao_iniciar.config(state="disabled")
    botao_parar.config(state="disabled")
    botao_cancelar.config(state="disabled")
    botao_arquivo.config(state="normal")

def cancelar_processo(status_label, botao_iniciar, botao_cancelar, botao_parar, botao_arquivo):
    parar_flag.set()
    status_label.config(text="❌ Processamento cancelado sem salvar.")
    botao_iniciar.config(state="disabled")
    botao_parar.config(state="disabled")
    botao_cancelar.config(state="disabled")
    botao_arquivo.config(state="normal")

def main():
    root = tk.Tk()
    root.title("Consultar Acordo - Etapa 2")
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

    botao_iniciar = ttk.Button(frame, text="Iniciar", state="disabled")
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
