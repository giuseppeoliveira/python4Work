import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from datetime import datetime

def detectar_delimitador(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        primeira_linha = f.readline()
        if ';' in primeira_linha:
            return ';'
        elif ',' in primeira_linha:
            return ','
        elif '\t' in primeira_linha:
            return '\t'
        else:
            return ','  # padrão

def salvar_log(erros):
    if not erros:
        return
    nome_log = "log_conversao.txt"
    with open(nome_log, "a", encoding="utf-8") as f:
        f.write(f"\n[LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        for erro in erros:
            f.write(f"{erro}\n")

def converter_em_thread(caminhos_csv, pasta_destino, progresso_var, barra, botao):
    total = len(caminhos_csv)
    sucesso = 0
    erros = []

    for i, caminho_csv in enumerate(caminhos_csv, start=1):
        try:
            delimitador = detectar_delimitador(caminho_csv)
            df = pd.read_csv(caminho_csv, delimiter=delimitador)

            # Corrigir cabeçalhos
            df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", '')

            nome_arquivo = os.path.splitext(os.path.basename(caminho_csv))[0] + '.xlsx'
            caminho_xlsx = os.path.join(pasta_destino, nome_arquivo)

            df.to_excel(caminho_xlsx, index=False)
            sucesso += 1

        except Exception as e:
            erros.append(f"{os.path.basename(caminho_csv)}: {str(e)}")

        progresso_var.set((i / total) * 100)
        barra.update()

    salvar_log(erros)

    resumo = f"{sucesso} arquivo(s) convertido(s) com sucesso."
    if erros:
        resumo += f"\n\n{len(erros)} erro(s) ocorreram. Detalhes salvos em 'log_conversao.txt'."

    messagebox.showinfo("Resultado da Conversão", resumo)
    botao.config(state="normal")

def iniciar_conversao():
    caminhos_csv = filedialog.askopenfilenames(
        title="Selecione um ou mais arquivos CSV",
        filetypes=[("Arquivos CSV", "*.csv")]
    )

    if not caminhos_csv:
        return

    pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino")

    if not pasta_destino:
        return

    botao_converter.config(state="disabled")
    threading.Thread(
        target=converter_em_thread,
        args=(caminhos_csv, pasta_destino, progresso_var, barra_progresso, botao_converter),
        daemon=True
    ).start()

# Interface Gráfica
root = tk.Tk()
root.title("Conversor CSV para XLSX")
root.geometry("480x220")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill='both')

label = ttk.Label(frame, text="Selecione arquivos CSV e escolha onde salvar os arquivos XLSX.")
label.pack(pady=(0, 10))

botao_converter = ttk.Button(frame, text="Selecionar e Converter", command=iniciar_conversao)
botao_converter.pack(pady=5)

progresso_var = tk.DoubleVar()
barra_progresso = ttk.Progressbar(frame, variable=progresso_var, maximum=100)
barra_progresso.pack(fill='x', pady=(10, 0))

rodape = ttk.Label(frame, text="Os erros (se houver) serão salvos em 'log_conversao.txt'")
rodape.pack(pady=(15, 0))

root.mainloop()
