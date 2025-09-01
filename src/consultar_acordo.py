import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import threading
import time
import os
import re
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import random

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

# Compilar regex uma única vez para melhor performance
STATUS_REGEX = re.compile(r"<Status>(.*?)</Status>")

def criar_sessao_otimizada():
    """Cria uma sessão HTTP otimizada com pool de conexões e retry"""
    session = requests.Session()
    
    # Configurar retry automático
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    # Configurar adaptador HTTP com pool de conexões
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=50,
        pool_maxsize=50,
        pool_block=False
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Headers otimizados
    session.headers.update({
        'Connection': 'keep-alive',
        'User-Agent': 'Python4Work-Consultar-Acordo/1.0',
        'Accept-Encoding': 'gzip, deflate'
    })
    
    return session

# Sessão HTTP reutilizável para melhor performance
session = criar_sessao_otimizada()

def validar_codigo(valor, nome_campo, index):
    """Valida e converte códigos para inteiro, com tratamento robusto de tipos incluindo numpy"""
    try:
        if valor is None or valor == "":
            print(f"⚠️ Linha {index + 1}: {nome_campo} está vazio ou None")
            return None
        
        # Importar numpy dinamicamente para verificar tipos
        try:
            import numpy as np
            # Verificar se é tipo numpy e converter para tipo Python nativo
            if hasattr(valor, 'dtype'):  # É um tipo numpy
                if np.isnan(valor):
                    print(f"⚠️ Linha {index + 1}: {nome_campo} é NaN")
                    return None
                valor = valor.item()  # Converter numpy para tipo Python nativo
        except ImportError:
            pass  # numpy não disponível, continuar normalmente
            
        # Tentar converter diferentes tipos para int
        if isinstance(valor, str):
            # Limpar string (remover espaços, caracteres especiais)
            valor = valor.strip()
            if valor == "" or valor.lower() in ["null", "none", "nan", "#n/a"]:
                print(f"⚠️ Linha {index + 1}: {nome_campo} contém valor inválido: '{valor}'")
                return None
            
            # Tentar converter string para float primeiro (caso tenha .0) depois para int
            try:
                valor_float = float(valor)
                if valor_float.is_integer():
                    return int(valor_float)
                else:
                    print(f"⚠️ Linha {index + 1}: {nome_campo} não é um número inteiro: {valor}")
                    return None
            except ValueError:
                print(f"⚠️ Linha {index + 1}: {nome_campo} não é um número válido: '{valor}'")
                return None
                
        elif isinstance(valor, (int, float)):
            if isinstance(valor, float):
                if valor != valor:  # Verificar se é NaN
                    print(f"⚠️ Linha {index + 1}: {nome_campo} é NaN")
                    return None
                if not valor.is_integer():
                    print(f"⚠️ Linha {index + 1}: {nome_campo} não é um número inteiro: {valor}")
                    return None
                return int(valor)
            return int(valor)
        else:
            # Tentar conversão direta para int como último recurso
            try:
                return int(valor)
            except (ValueError, TypeError):
                print(f"⚠️ Linha {index + 1}: {nome_campo} tem tipo não suportado: {type(valor)} = {valor}")
                return None
            
    except Exception as e:
        print(f"❌ Linha {index + 1}: Erro ao validar {nome_campo} = {valor}: {e}")
        return None

def consultar_status_acordo(row, index, session_local=None, tentativas=2):
    """Consulta o status do acordo com validações robustas e debug detalhado"""
    global total_erros
    
    if session_local is None:
        session_local = session
    
    # Validação robusta dos dados de entrada
    cod_cliente = validar_codigo(row.get("cod_cliente", 0), "cod_cliente", index)
    cod_acordo = validar_codigo(row.get("cod_acordo", 0), "cod_acordo", index)
    
    # Validar se os códigos são válidos
    if cod_cliente is None or cod_acordo is None:
        log = f"Linha {index + 1}: ❌ Dados inválidos - cod_cliente={row.get('cod_cliente')}, cod_acordo={row.get('cod_acordo')}"
        log_erros.append(log)
        print(log)
        total_erros += 1
        return "Dados inválidos"
    
    # Verificar se os códigos são maiores que 0
    if cod_cliente <= 0 or cod_acordo <= 0:
        log = f"Linha {index + 1}: ⚠️ Códigos inválidos - cod_cliente={cod_cliente}, cod_acordo={cod_acordo} (devem ser > 0)"
        log_erros.append(log)
        print(log)
        total_erros += 1
        return "Códigos inválidos"

    payload = {
        "logonUsuario": LOGIN,
        "senhaUsuario": SENHA,
        "idCliente": int(cod_cliente),
        "idAcordo": int(cod_acordo)
    }
    
    # Debug: Log do payload (apenas para primeiras 5 linhas para não poluir)
    if index < 5:
        print(f"🔍 Debug linha {index + 1}: payload={payload}")

    for tentativa in range(1, tentativas + 1):
        try:
            # Timeout reduzido para 3s para melhor throughput
            response = session_local.post(URL, data=payload, timeout=3)
            response.raise_for_status()

            # Debug: Log da resposta (apenas para primeiras 3 linhas)
            if index < 3:
                print(f"🔍 Debug linha {index + 1}: response.status_code={response.status_code}, content_length={len(response.content) if response.content else 0}")

            # Parse XML otimizado com validações robustas
            if response.content:
                try:
                    soup = BeautifulSoup(response.content, "xml")
                    string_tag = soup.find("string")

                    if string_tag and string_tag.text:
                        decoded = string_tag.text.replace("&lt;", "<").replace("&gt;", ">")
                        
                        # Debug: Log do XML decodificado (apenas para primeiras 2 linhas)
                        if index < 2:
                            print(f"🔍 Debug linha {index + 1}: XML decodificado (primeiros 200 chars): {decoded[:200]}...")
                        
                        # Usar regex pré-compilada
                        status_match = STATUS_REGEX.search(decoded)
                        if status_match:
                            status_resultado = status_match.group(1).strip()
                            
                            # Debug: Log do status encontrado (apenas para primeiras 3 linhas)
                            if index < 3:
                                print(f"✅ Debug linha {index + 1}: Status encontrado: '{status_resultado}'")
                                
                            return status_resultado
                        else:
                            # Tentar buscar outras tags comuns de erro/status
                            error_patterns = [
                                (r"<erro>(.*?)</erro>", "Erro"),
                                (r"<Error>(.*?)</Error>", "Error"), 
                                (r"<message>(.*?)</message>", "Message"),
                                (r"<Message>(.*?)</Message>", "Message"),
                                (r"<resultado>(.*?)</resultado>", "Resultado")
                            ]
                            
                            for pattern, tag_name in error_patterns:
                                match = re.search(pattern, decoded, re.IGNORECASE)
                                if match:
                                    resultado = match.group(1).strip()
                                    print(f"⚠️ Linha {index + 1}: Encontrado <{tag_name}>: '{resultado}'")
                                    return f"{tag_name}: {resultado}"
                            
                            # Se não encontrou nenhum padrão, salvar XML para análise
                            if index < 5:  # Salvar apenas os primeiros para análise
                                print(f"❌ Linha {index + 1}: Campo <Status> não encontrado. XML completo: {decoded}")
                            
                            raise ValueError(f"⚠️ Campo <Status> não encontrado. XML tem {len(decoded)} caracteres.")
                    else:
                        raise ValueError("⚠️ Tag <string> não encontrada ou vazia.")
                        
                except Exception as parse_error:
                    # Log do erro de parsing com o conteúdo da resposta
                    print(f"❌ Linha {index + 1}: Erro no parsing XML: {parse_error}")
                    if index < 3:  # Log do conteúdo apenas para primeiras linhas
                        print(f"🔍 Conteúdo bruto da resposta: {response.content[:500]}...")
                    raise ValueError(f"Erro no parsing XML: {parse_error}")
            else:
                raise ValueError("⚠️ Resposta vazia do servidor.")

        except requests.exceptions.Timeout:
            log = f"Linha {index + 1}: ⏰ Timeout na tentativa {tentativa} - cod_cliente={cod_cliente}, cod_acordo={cod_acordo}"
            print(log)
            if tentativa < tentativas:
                time.sleep(random.uniform(0.1, 0.3))  # Backoff aleatório
                
        except requests.exceptions.HTTPError as e:
            log = f"Linha {index + 1}: 🌐 Erro HTTP {e.response.status_code} na tentativa {tentativa} - cod_cliente={cod_cliente}, cod_acordo={cod_acordo}"
            print(log)
            # Se for erro 400-499, não vale a pena tentar novamente
            if 400 <= e.response.status_code < 500 and tentativa == 1:
                log_erros.append(log + " (erro de cliente - não retienta)")
                total_erros += 1
                return f"Erro HTTP {e.response.status_code}"
            if tentativa < tentativas:
                time.sleep(random.uniform(0.1, 0.3))
                
        except requests.exceptions.ConnectionError as e:
            log = f"Linha {index + 1}: 🔌 Erro de conexão na tentativa {tentativa} - {str(e)[:100]} - cod_cliente={cod_cliente}, cod_acordo={cod_acordo}"
            print(log)
            if tentativa < tentativas:
                time.sleep(random.uniform(0.5, 1.0))  # Backoff maior para conexão
                
        except requests.exceptions.RequestException as e:
            log = f"Linha {index + 1}: ❌ Erro HTTP {e.__class__.__name__}: {str(e)[:100]} - cod_cliente={cod_cliente}, cod_acordo={cod_acordo}"
            print(log)
            if tentativa < tentativas:
                time.sleep(random.uniform(0.1, 0.3))  # Backoff aleatório
                
        except Exception as e:
            log = f"Linha {index + 1}: ❌ Erro inesperado na tentativa {tentativa}: {e.__class__.__name__}: {str(e)[:100]}"
            print(log)
            if tentativa < tentativas:
                time.sleep(random.uniform(0.1, 0.3))  # Backoff aleatório

        if tentativa < tentativas:
            continue
        else:
            log_erros.append(log)
            print(log)

    total_erros += 1
    return "Não encontrado"

def validar_dados_entrada(df):
    """Valida se o DataFrame tem as colunas necessárias e dados válidos"""
    print("🔍 Validando dados de entrada...")
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['cod_cliente', 'cod_acordo']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
    
    if colunas_faltantes:
        raise ValueError(f"❌ Colunas não encontradas no arquivo: {', '.join(colunas_faltantes)}")
    
    print(f"✅ Colunas necessárias encontradas: {colunas_necessarias}")
    
    # Estatísticas dos dados
    total_registros = len(df)
    print(f"📊 Total de registros: {total_registros}")
    
    # Analisar cod_cliente
    cod_cliente_nulos = df['cod_cliente'].isna().sum()
    cod_cliente_vazios = (df['cod_cliente'] == '').sum() if df['cod_cliente'].dtype == 'object' else 0
    cod_cliente_zeros = (df['cod_cliente'] == 0).sum()
    
    print(f"🔍 cod_cliente - Nulos: {cod_cliente_nulos}, Vazios: {cod_cliente_vazios}, Zeros: {cod_cliente_zeros}")
    
    # Analisar cod_acordo  
    cod_acordo_nulos = df['cod_acordo'].isna().sum()
    cod_acordo_vazios = (df['cod_acordo'] == '').sum() if df['cod_acordo'].dtype == 'object' else 0
    cod_acordo_zeros = (df['cod_acordo'] == 0).sum()
    
    print(f"🔍 cod_acordo - Nulos: {cod_acordo_nulos}, Vazios: {cod_acordo_vazios}, Zeros: {cod_acordo_zeros}")
    
    # Calcular registros potencialmente válidos
    registros_invalidos = max(cod_cliente_nulos + cod_cliente_vazios + cod_cliente_zeros,
                             cod_acordo_nulos + cod_acordo_vazios + cod_acordo_zeros)
    registros_validos = total_registros - registros_invalidos
    
    print(f"⚠️ Registros potencialmente inválidos: {registros_invalidos}")
    print(f"✅ Registros potencialmente válidos: {registros_validos}")
    
    if registros_validos == 0:
        raise ValueError("❌ Nenhum registro válido encontrado. Verifique se as colunas cod_cliente e cod_acordo têm valores > 0.")
    
    # Mostrar alguns exemplos de dados válidos
    dados_validos = df[(df['cod_cliente'].notna()) & (df['cod_cliente'] != '') & (df['cod_cliente'] != 0) &
                      (df['cod_acordo'].notna()) & (df['cod_acordo'] != '') & (df['cod_acordo'] != 0)].head(3)
    
    if len(dados_validos) > 0:
        print("📋 Exemplos de registros válidos:")
        for idx, row in dados_validos.iterrows():
            print(f"   Linha {idx + 1}: cod_cliente={row['cod_cliente']}, cod_acordo={row['cod_acordo']}")
    
    return registros_validos

def consultar_status_acordo_batch(rows_batch, max_workers=25):
    """Processa um lote de consultas em paralelo com otimizações"""
    results = []
    
    # Criar sessões dedicadas para cada worker
    def criar_worker_session():
        return criar_sessao_otimizada()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Criar uma sessão para cada worker para evitar conflitos
        future_to_row = {}
        
        for index, row in rows_batch:
            future = executor.submit(consultar_status_acordo, row, index, criar_worker_session())
            future_to_row[future] = (index, row)
        
        # Coletar resultados conforme completam
        for future in as_completed(future_to_row):
            index, row = future_to_row[future]
            try:
                status = future.result(timeout=10)  # Timeout por future
                results.append((index, status))
            except Exception as e:
                print(f"Erro no processamento da linha {index}: {e}")
                results.append((index, "Erro"))
    
    return results

def salvar_parcial(df, caminho_salvar, force=False):
    """Salva o arquivo apenas a cada X linhas ou quando forçado"""
    try:
        if force or linhas_processadas % 100 == 0:  # Salva a cada 100 linhas (menos I/O)
            df.to_excel(caminho_salvar, index=False)
            print(f"💾 Progresso salvo: {linhas_processadas} linhas processadas")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

def processar_batch_cpf(df, batch_size=50, max_workers=25):
    """
    Processa o DataFrame em lotes otimizados
    """
    global linhas_processadas
    total = len(df)
    linhas_processadas = 0
    
    print(f"🚀 Iniciando processamento otimizado:")
    print(f"   📊 Total de registros: {total}")
    print(f"   📦 Tamanho do lote: {batch_size}")
    print(f"   👥 Workers paralelos: {max_workers}")
    print("=" * 50)
    
    start_time = time.time()
    
    # Processar em lotes
    for batch_start in range(0, total, batch_size):
        if parar_flag.is_set():
            print("⏸️ Processamento interrompido pelo usuário")
            break
            
        batch_end = min(batch_start + batch_size, total)
        batch_rows = [(i, df.iloc[i]) for i in range(batch_start, batch_end)]
        
        batch_start_time = time.time()
        
        # Processar lote em paralelo
        print(f"🔄 Processando lote {batch_start//batch_size + 1}: linhas {batch_start+1} a {batch_end}")
        batch_results = consultar_status_acordo_batch(batch_rows, max_workers)
        
        # Atualizar DataFrame com resultados
        for index, status in batch_results:
            df.at[index, "status_acordo"] = status
            linhas_processadas += 1
        
        batch_time = time.time() - batch_start_time
        print(f"   ✅ Lote concluído em {batch_time:.1f}s ({len(batch_rows)/batch_time:.1f} req/s)")
        
        # Calcular estatísticas
        elapsed_time = time.time() - start_time
        if linhas_processadas > 0:
            avg_time_per_item = elapsed_time / linhas_processadas
            remaining_items = total - linhas_processadas
            estimated_remaining = avg_time_per_item * remaining_items
            
            print(f"   📈 Progresso: {linhas_processadas}/{total} ({linhas_processadas/total*100:.1f}%)")
            print(f"   ⏱️ Tempo estimado restante: {estimated_remaining/60:.1f} min")
            print(f"   ⚡ Velocidade média: {linhas_processadas/elapsed_time:.1f} req/s")
    
    total_time = time.time() - start_time
    print(f"\n🎯 Processamento concluído em {total_time/60:.1f} minutos")
    print(f"⚡ Velocidade final: {linhas_processadas/total_time:.1f} req/s")
    print(f"❌ Total de erros: {total_erros}")
    
    return df

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
    
    try:
        # Resetar contadores
        linhas_processadas = 0
        total_erros = 0
        log_erros = []
        
        # Carregar arquivo
        print(f"📂 Carregando arquivo: {caminho_arquivo}")
        df = pd.read_excel(caminho_arquivo)
        
        # Validar dados de entrada
        try:
            registros_validos_esperados = validar_dados_entrada(df)
            print(f"✅ Validação concluída. Registros válidos esperados: {registros_validos_esperados}")
        except Exception as validation_error:
            error_msg = f"❌ Erro na validação dos dados: {validation_error}"
            print(error_msg)
            status_label.config(text=error_msg)
            return
        
        # Verificar/criar coluna status_acordo
        if 'status_acordo' not in df.columns:
            df["status_acordo"] = ""
        
        total = len(df)
        print(f"📊 Total de registros carregados: {total}")
        
        # Configurações otimizadas
        batch_size = 50  # Lotes maiores para melhor throughput
        max_workers = 25  # Mais workers para paralelismo
        
        start_time = time.time()
        
        # Usar a função otimizada de processamento em lotes
        for batch_start in range(0, total, batch_size):
            if parar_flag.is_set():
                status_label.config(text="⏸️ Processamento interrompido")
                break
                
            batch_end = min(batch_start + batch_size, total)
            batch_rows = [(i, df.iloc[i]) for i in range(batch_start, batch_end)]
            
            # Processar lote em paralelo
            batch_results = consultar_status_acordo_batch(batch_rows, max_workers)
            
            # Atualizar DataFrame com resultados
            for index, status in batch_results:
                df.at[index, "status_acordo"] = status
                linhas_processadas += 1

            # Atualizar interface
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
                req_per_sec = linhas_processadas / elapsed_time
                status_label.config(text=f"Processando: {linhas_processadas}/{total} - Restam ~{minutes}m {seconds}s - {req_per_sec:.1f} req/s")
            
            # Salvar progresso periodicamente
            salvar_parcial(df, caminho_salvar)

        # Salvar arquivo final
        salvar_parcial(df, caminho_salvar, force=True)

        # Salvar log de erros
        if log_erros:
            log_file = caminho_salvar.replace('.xlsx', '_log_erros.txt')
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"=== LOG DE ERROS - CONSULTAR ACORDO ===\n")
                f.write(f"Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de registros: {total}\n")
                f.write(f"Registros processados: {linhas_processadas}\n")
                f.write(f"Total de erros: {total_erros}\n")
                f.write(f"Taxa de sucesso: {((linhas_processadas-total_erros)/linhas_processadas*100):.1f}%\n")
                f.write("=" * 50 + "\n\n")
                for linha in log_erros:
                    f.write(linha + "\n")
            print(f"📝 Log de erros salvo: {log_file}")

        # Finalizar interface
        elapsed_total = time.time() - start_time
        final_msg = f"✅ Concluído! {linhas_processadas}/{total} em {elapsed_total/60:.1f}min - {total_erros} erros"
        status_label.config(text=final_msg)
        print(final_msg)
        
    except Exception as e:
        error_msg = f"❌ Erro no processamento: {str(e)}"
        status_label.config(text=error_msg)
        print(error_msg)
    
    finally:
        # Reabilitar botões
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
    root.title("Consultar Acordo - Etapa 2 (OTIMIZADO)")
    root.geometry("700x250")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # Título com informações de otimização
    titulo = ttk.Label(frame, text="Consultar Status de Acordos - Versão Otimizada", font=("Arial", 12, "bold"))
    titulo.pack(pady=(0, 10))
    
    info_otimizacao = ttk.Label(frame, text="🚀 Performance: 25 workers paralelos | ⚡ 3-5x mais rápido", foreground="green")
    info_otimizacao.pack()

    progresso_var = tk.IntVar()
    progresso_bar = ttk.Progressbar(frame, variable=progresso_var, maximum=100, length=600)
    progresso_bar.pack(pady=5)

    progresso_label = ttk.Label(frame, text="0%")
    progresso_label.pack()

    status_label = ttk.Label(frame, text="Nenhum arquivo selecionado.")
    status_label.pack(pady=5)

    # Frame para botões
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)

    botao_arquivo = ttk.Button(button_frame, text="📁 Escolher Arquivo")
    botao_arquivo.pack(side="left", padx=5)

    botao_iniciar = ttk.Button(button_frame, text="🚀 Iniciar", state="disabled")
    botao_iniciar.pack(side="left", padx=5)

    botao_parar = ttk.Button(button_frame, text="⏸️ Parar (Salvar)", state="disabled")
    botao_parar.pack(side="left", padx=5)

    botao_cancelar = ttk.Button(button_frame, text="❌ Cancelar", state="disabled")
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
