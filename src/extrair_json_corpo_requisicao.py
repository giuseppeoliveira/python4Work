import pandas as pd
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import time

def extrair_e_salvar():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo XLSX de entrada",
        filetypes=[("Arquivos Excel", "*.xlsx")]
    )

    if not caminho_arquivo:
        return

    try:
        df = pd.read_excel(caminho_arquivo)

        if 'corpo_requisicao' not in df.columns:
            messagebox.showerror("Erro", "A coluna 'corpo_requisicao' não foi encontrada.")
            return

        total = len(df)
        registros = []
        falhas = []

        barra_progresso["maximum"] = total
        progresso_var.set(0)
        tempo_inicio = time.time()

        for index, linha in df.iterrows():
            corpo = linha['corpo_requisicao']
            try:
                if isinstance(corpo, str):
                    corpo_json = json.loads(corpo)

                    carga = corpo_json.get("carga", {})
                    idCarga = carga.get('idCarga')

                    # Ignorar linha se idCarga for vazio/None/NaN
                    if idCarga is None or (isinstance(idCarga, float) and pd.isna(idCarga)):
                        raise ValueError("idCarga vazio - linha ignorada")

                    origem = carga.get('origem')

                    # Remove prefixo "CGFF" se existir
                    if isinstance(origem, str) and origem.startswith("CGFF"):
                        origem = origem[4:]

                    # Pega nmArquivo de clientesArquivo[0], senão da carga
                    nmArquivo = None
                    clientesArquivo = corpo_json.get('clientesArquivo', [])
                    if isinstance(clientesArquivo, list) and len(clientesArquivo) > 0:
                        nmArquivo = clientesArquivo[0].get('nmArquivo')

                    if not nmArquivo:
                        nmArquivo = carga.get('nmArquivo')

                    registros.append({
                        'idCarga': idCarga,
                        'origem': origem,
                        'nmArquivo': nmArquivo,
                        'data_hora': linha.get('data_hora')  # pode ser None se não existir
                    })

                else:
                    raise ValueError("Valor não é uma string JSON")

            except Exception as e:
                falhas.append(f"Linha {index+2}: {str(e)}")

            progresso_var.set(index + 1)
            barra_progresso.update()
            tempo_passado = time.time() - tempo_inicio
            estimativa_total = (tempo_passado / (index + 1)) * total
            restante = estimativa_total - tempo_passado
            tempo_label.config(text=f"{index + 1}/{total} | Estimado: {int(restante)}s restantes")

        # Criar DataFrame só com os registros válidos
        novo_df = pd.DataFrame(registros)

        # Escolher onde salvar o novo arquivo
        caminho_saida = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")],
            title="Salvar como"
        )

        if not caminho_saida:
            return

        novo_df.to_excel(caminho_saida, index=False)

        # Salvar log de falhas
        if falhas:
            with open("log_extracao.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
                for linha in falhas:
                    f.write(linha + "\n")

        msg = f"Arquivo salvo com sucesso em:\n{caminho_saida}"
        if falhas:
            msg += f"\n\n⚠ {len(falhas)} linha(s) com erro foram registradas em 'log_extracao.txt'."
        messagebox.showinfo("Concluído", msg)
        tempo_label.config(text="Processo finalizado.")
        progresso_var.set(0)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")

# Interface gráfica
def iniciar_interface():
    global progresso_var, barra_progresso, tempo_label

    root = tk.Tk()
    root.title("Extrator de JSON - corpo_requisicao")
    root.geometry("520x250")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True, fill='both')

    label = ttk.Label(frame, text="1. Selecione o XLSX com a coluna 'corpo_requisicao'\n2. Escolha onde salvar com nome desejado")
    label.pack(pady=(0, 10))

    botao = ttk.Button(frame, text="Selecionar Arquivo e Extrair", command=extrair_e_salvar)
    botao.pack(pady=5)

    progresso_var = tk.DoubleVar()
    barra_progresso = ttk.Progressbar(frame, variable=progresso_var, maximum=100)
    barra_progresso.pack(fill='x', pady=10)

    tempo_label = ttk.Label(frame, text="Aguardando início...")
    tempo_label.pack()

    rodape = ttk.Label(frame, text="Falhas serão salvas em 'log_extracao.txt'", foreground="gray")
    rodape.pack(pady=(15, 0))

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
