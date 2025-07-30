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
        response = requests.post(URL_DIVIDA, data=payload, timeout=10)
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
        print(f"[ERRO consultar_easycollector] CPF {cpf}: {e}")
        return 0, 0, []

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

    for i, row in df.iterrows():
        if cancelar_evento.is_set():
            status_label.config(text="Processo cancelado. Nenhuma alteração salva.")
            print("[INFO] Processo cancelado pelo usuário. Nenhuma alteração salva.")
            return
        if parar_evento.is_set():
            status_label.config(text=f"Processo parado. Salvando progresso até linha {i}...")
            print(f"[INFO] Processo parado pelo usuário. Salvando progresso até linha {i}...")
            df.iloc[:i].to_excel(caminho_salvar, index=False, engine='openpyxl')
            progresso_var.set(100)
            progresso_label.config(text="100%")
            messagebox.showinfo("Interrompido", f"Progresso salvo até a linha {i} em:\n{caminho_salvar}")
            return

        cod_acordo = row.get("cod_acordo", "0")
        cod_cliente = row.get("cod_cliente", "0")

        if cod_acordo != "0" or cod_cliente != "0":
            # Já possui os códigos → marcar como Excluir
            df.at[i, "status"] = "Excluir"
            df.at[i, "observacao"] = "Em Duplicidade"
            print(f"[Linha {i+1}/{total}] CPF: {row.get('cpf', '')} | cod_acordo={cod_acordo}, cod_cliente={cod_cliente} -> Excluir")
            continue

        # Para registros com cod_acordo e cod_cliente igual a 0, tenta atualizar
        cpf_raw = row.get("cpf", "")
        cpf = limpar_cpf(cpf_raw)

        if not cpf or cpf == "00000000000":
            print(f"[Linha {i+1}] CPF inválido ou vazio ('{cpf_raw}'), pulando...")
            df.at[i, "status"] = ""
            df.at[i, "observacao"] = ""
            continue

        data_venc = str(row.get("data_vencimento", ""))[:10]

        id_cliente, id_acordo, datas = consultar_easycollector(cpf, LOGIN_FIXO, SENHA_FIXO)

        alterou = False

        if id_cliente != 0:
            df.at[i, "cod_cliente"] = str(id_cliente)
            alterou = True

        if id_acordo != 0:
            df.at[i, "cod_acordo"] = str(id_acordo)
            alterou = True

        if alterou and (df.at[i, "cod_cliente"] != "0" or df.at[i, "cod_acordo"] != "0"):
            df.at[i, "status"] = "Update"
            df.at[i, "observacao"] = "Atualizado"
        elif df.at[i, "cod_cliente"] == "0" and df.at[i, "cod_acordo"] == "0":
            df.at[i, "status"] = "Investigar"
            df.at[i, "observacao"] = "Não Encontrado"
        else:
            df.at[i, "status"] = ""
            df.at[i, "observacao"] = ""


        print(f"[Linha {i+1}/{total}] CPF: {cpf} | cod_cliente: {id_cliente} | cod_acordo: {id_acordo} | status: {df.at[i, 'status']}")

        progresso = int((i + 1) / total * 100)
        progresso_var.set(progresso)
        progresso_label.config(text=f"{progresso}%")

        tempo_passado = time.time() - tempo_inicio
        if i > 0:
            tempo_estimado_restante = (tempo_passado / (i + 1)) * (total - i - 1)
            minutos = int(tempo_estimado_restante // 60)
            segundos = int(tempo_estimado_restante % 60)
            status_label.config(text=f"Processando: {i+1}/{total} - Tempo estimado restante: {minutos}m {segundos}s")
        else:
            status_label.config(text=f"Processando: {i+1}/{total} - Calculando tempo restante...")

        time.sleep(0.01)

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
