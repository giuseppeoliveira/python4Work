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

# Contador para debug - analisa apenas os primeiros 5 CPFs em detalhes
debug_counter = 0
MAX_DEBUG_LOGS = 5

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
    global debug_counter
    
    payload = {
        "logonUsuario": login,
        "senhaUsuario": senha,
        "cpfCnpj": cpf
    }
    try:
        # Reduzido timeout de 10s para 5s para melhor performance
        response = session.post(URL_DIVIDA, data=payload, timeout=5)
        response.raise_for_status()
        
        # Debug detalhado para os primeiros CPFs
        if debug_counter < MAX_DEBUG_LOGS:
            print(f"\n[DEBUG #{debug_counter+1}] ===== ANÁLISE DETALHADA CPF: {cpf} =====")
            print(f"[DEBUG #{debug_counter+1}] Response Status: {response.status_code}")
            print(f"[DEBUG #{debug_counter+1}] Response Content (primeiros 1000 chars):\n{response.text[:1000]}...")
            debug_counter += 1
        
        # Parsing melhorado usando delimitadores específicos
        response_text = response.text
        
        # Método 1: Usar delimitadores específicos baseados na sua observação
        blocos_personalizados = []
        if "<NmCedente>" in response_text and "</PercentualDescontoJuros>" in response_text:
            # Dividir por início de bloco
            partes = response_text.split("<NmCedente>")
            for i, parte in enumerate(partes[1:], 1):  # Pular primeira parte vazia
                # Encontrar fim do bloco
                if "</PercentualDescontoJuros>" in parte:
                    fim_bloco = parte.find("</PercentualDescontoJuros>") + len("</PercentualDescontoJuros>")
                    bloco_completo = "<NmCedente>" + parte[:fim_bloco]
                    blocos_personalizados.append(bloco_completo)
                    
                    if debug_counter <= MAX_DEBUG_LOGS:
                        print(f"[DEBUG] CPF {cpf}: Bloco personalizado {i} extraído (tamanho: {len(bloco_completo)} chars)")
        
        # Parsing com BeautifulSoup nos blocos personalizados
        soup = BeautifulSoup(response.content, "xml")
        
        # Procurar por todos os blocos DividaAtiva (método original)
        divida_ativa_blocks = soup.find_all("DividaAtiva")
        
        if debug_counter <= MAX_DEBUG_LOGS:
            print(f"[DEBUG] CPF {cpf}: BeautifulSoup encontrou {len(divida_ativa_blocks)} blocos DividaAtiva")
            print(f"[DEBUG] CPF {cpf}: Método personalizado encontrou {len(blocos_personalizados)} blocos")
        
        # Coletar dados usando ambos os métodos
        id_cliente_vals = []
        id_acordo_vals = []
        data_vencs = []
        
        # Método 1: Processar blocos personalizados (baseado na sua observação)
        for i, bloco_texto in enumerate(blocos_personalizados):
            if debug_counter <= MAX_DEBUG_LOGS:
                print(f"[DEBUG] CPF {cpf}: Processando bloco personalizado {i+1}")
            
            # Usar BeautifulSoup no bloco individual
            bloco_soup = BeautifulSoup(bloco_texto, "xml")
            
            # Extrair IdCliente
            id_cliente_elem = bloco_soup.find("IdCliente")
            if id_cliente_elem and id_cliente_elem.text and id_cliente_elem.text.strip().isdigit():
                val = int(id_cliente_elem.text.strip())
                if val != 0:
                    id_cliente_vals.append(val)
                    if debug_counter <= MAX_DEBUG_LOGS:
                        print(f"[DEBUG] CPF {cpf} Bloco personalizado {i+1}: IdCliente={val}")
            
            # Extrair IdAcordo
            id_acordo_elem = bloco_soup.find("IdAcordo")
            if id_acordo_elem and id_acordo_elem.text and id_acordo_elem.text.strip().isdigit():
                val = int(id_acordo_elem.text.strip())
                if val != 0:
                    id_acordo_vals.append(val)
                    if debug_counter <= MAX_DEBUG_LOGS:
                        print(f"[DEBUG] CPF {cpf} Bloco personalizado {i+1}: IdAcordo={val}")
            
            # Extrair DataVencimento
            data_venc_elem = bloco_soup.find("DataVencimento")
            if data_venc_elem and data_venc_elem.text and data_venc_elem.text.strip():
                data_vencs.append(data_venc_elem.text.strip())
        
        # Método 2: Processar blocos DividaAtiva tradicionais (fallback)
        if not blocos_personalizados and divida_ativa_blocks:
            if debug_counter <= MAX_DEBUG_LOGS:
                print(f"[DEBUG] CPF {cpf}: Usando método tradicional DividaAtiva como fallback")
                
            for i, bloco in enumerate(divida_ativa_blocks):
                # Extrair IdCliente do bloco atual
                id_cliente_elem = bloco.find("IdCliente")
                if id_cliente_elem and id_cliente_elem.text and id_cliente_elem.text.strip().isdigit():
                    val = int(id_cliente_elem.text.strip())
                    if val != 0:
                        id_cliente_vals.append(val)
                        if debug_counter <= MAX_DEBUG_LOGS:
                            print(f"[DEBUG] CPF {cpf} Bloco DividaAtiva {i+1}: IdCliente={val}")
                
                # Extrair IdAcordo do bloco atual
                id_acordo_elem = bloco.find("IdAcordo")
                if id_acordo_elem and id_acordo_elem.text and id_acordo_elem.text.strip().isdigit():
                    val = int(id_acordo_elem.text.strip())
                    if val != 0:
                        id_acordo_vals.append(val)
                        if debug_counter <= MAX_DEBUG_LOGS:
                            print(f"[DEBUG] CPF {cpf} Bloco DividaAtiva {i+1}: IdAcordo={val}")
                
                # Extrair DataVencimento do bloco atual
                data_venc_elem = bloco.find("DataVencimento")
                if data_venc_elem and data_venc_elem.text and data_venc_elem.text.strip():
                    data_vencs.append(data_venc_elem.text.strip())
        
        # Método 3: Busca global como último recurso
        if not id_cliente_vals and not id_acordo_vals:
            if debug_counter <= MAX_DEBUG_LOGS:
                print(f"[DEBUG] CPF {cpf}: Usando busca global como último recurso")
            
            # Buscar todos os elementos diretamente
            id_cliente_elements = soup.find_all("IdCliente")
            id_acordo_elements = soup.find_all("IdAcordo")
            
            for elem in id_cliente_elements:
                if elem.text and elem.text.strip().isdigit():
                    val = int(elem.text.strip())
                    if val != 0:
                        id_cliente_vals.append(val)
            
            for elem in id_acordo_elements:
                if elem.text and elem.text.strip().isdigit():
                    val = int(elem.text.strip())
                    if val != 0:
                        id_acordo_vals.append(val)
        
        # Remover duplicatas mantendo ordem
        id_cliente_vals = list(dict.fromkeys(id_cliente_vals))
        id_acordo_vals = list(dict.fromkeys(id_acordo_vals))
        
        # Lógica de seleção: prioriza o primeiro valor válido encontrado
        id_cliente = id_cliente_vals[0] if id_cliente_vals else 0
        id_acordo = id_acordo_vals[0] if id_acordo_vals else 0
        
        # Debug detalhado para primeiros CPFs
        if debug_counter <= MAX_DEBUG_LOGS:
            print(f"[RESULTADO] CPF {cpf}: IdCliente={id_cliente} (de {id_cliente_vals})")
            print(f"[RESULTADO] CPF {cpf}: IdAcordo={id_acordo} (de {id_acordo_vals})")
            print(f"[RESULTADO] CPF {cpf}: {len(data_vencs)} datas encontradas")
            if len(data_vencs) > 0:
                print(f"[RESULTADO] CPF {cpf}: Primeira data: {data_vencs[0]}")
        
        return id_cliente, id_acordo, data_vencs

    except Exception as e:
        print(f"❌ [ERRO] CPF {cpf}: {e}")
        return 0, 0, []

def processar_linha_cpf(row_data):
    """Processa uma única linha de CPF com logging melhorado"""
    i, row = row_data
    
    cod_acordo = row.get("cod_acordo", "0")
    cod_cliente = row.get("cod_cliente", "0")

    # Debug: Log linha sendo processada
    cpf_raw = row.get("cpf", "")
    cpf = limpar_cpf(cpf_raw)
    print(f"[Linha {i+1}] ===== PROCESSANDO CPF: {cpf} =====")
    print(f"[Linha {i+1}] Valores atuais - cod_cliente: {cod_cliente} | cod_acordo: {cod_acordo}")

    if cod_acordo != "0" or cod_cliente != "0":
        # Já possui os códigos → marcar como Excluir
        print(f"[Linha {i+1}] ✅ CPF {cpf}: Já possui códigos, marcando para exclusão")
        return i, "Excluir", "Em Duplicidade", cod_cliente, cod_acordo

    # Para registros com cod_acordo e cod_cliente igual a 0, tenta atualizar
    if not cpf or cpf == "00000000000":
        print(f"[Linha {i+1}] ❌ CPF inválido: {cpf_raw}")
        return i, "", "", "0", "0"

    print(f"[Linha {i+1}] 🔍 Consultando API para CPF: {cpf}")
    
    # Fazer consulta na API
    id_cliente, id_acordo, datas = consultar_easycollector(cpf, LOGIN_FIXO, SENHA_FIXO)

    print(f"[Linha {i+1}] 📡 API retornou - IdCliente: {id_cliente} | IdAcordo: {id_acordo} | Datas: {len(datas)}")

    alterou = False
    new_cod_cliente = cod_cliente
    new_cod_acordo = cod_acordo

    # Lógica melhorada de atualização
    if id_cliente != 0:
        new_cod_cliente = str(id_cliente)
        alterou = True
        print(f"[Linha {i+1}] ✅ IdCliente atualizado: {cod_cliente} → {new_cod_cliente}")

    if id_acordo != 0:
        new_cod_acordo = str(id_acordo)
        alterou = True
        print(f"[Linha {i+1}] ✅ IdAcordo atualizado: {cod_acordo} → {new_cod_acordo}")

    # Determinar status baseado nos resultados
    if alterou and (new_cod_cliente != "0" or new_cod_acordo != "0"):
        status = "Update"
        observacao = f"Atualizado - Cliente:{new_cod_cliente}, Acordo:{new_cod_acordo}"
        print(f"[Linha {i+1}] 🎯 STATUS: Update (dados encontrados e atualizados)")
    elif id_cliente == 0 and id_acordo == 0:
        # Só marca como "Não Encontrado" se a API não retornou NENHUM dado
        status = "Investigar"
        observacao = "Não Encontrado na API"
        print(f"[Linha {i+1}] ⚠️  STATUS: Investigar (nenhum dado encontrado na API)")
    else:
        status = ""
        observacao = ""
        print(f"[Linha {i+1}] ❓ STATUS: vazio (situação indefinida)")

    print(f"[Linha {i+1}] 📋 RESULTADO FINAL:")
    print(f"[Linha {i+1}]   • CPF: {cpf}")
    print(f"[Linha {i+1}]   • cod_cliente: {cod_cliente} → {new_cod_cliente}")
    print(f"[Linha {i+1}]   • cod_acordo: {cod_acordo} → {new_cod_acordo}")
    print(f"[Linha {i+1}]   • Status: {status}")
    print(f"[Linha {i+1}]   • Observação: {observacao}")
    print(f"[Linha {i+1}] " + "="*50)
    
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
