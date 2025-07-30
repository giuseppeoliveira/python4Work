"""
PYTHON4WORK - Interface Unificada
Centraliza todas as 4 funcionalidades do projeto em uma única interface.

Funcionalidades:
1. Consultar Acordo
2. Obter Dívida por CPF  
3. Extrair JSON do Corpo Requisição
4. Conversor CSV para XLSX
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import json
from datetime import datetime
import threading
import time
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações globais
LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")
URL = os.getenv("URL")
URL_DIVIDA = os.getenv("URL_DIVIDA")

# Verifica se as variáveis de ambiente foram carregadas
if not all([LOGIN, SENHA, URL, URL_DIVIDA]):
    print("⚠️ Aviso: Algumas variáveis de ambiente não foram encontradas. Algumas funcionalidades podem não funcionar.")

class Python4WorkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python4Work - Interface Unificada")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variáveis de controle
        self.progresso_var = tk.IntVar()
        self.parar_flag = threading.Event()
        self.cancelar_flag = threading.Event()
        
        self.criar_interface()
    
    def criar_interface(self):
        # Título principal
        titulo = tk.Label(self.root, text="🔧 Python4Work - Central de Ferramentas", 
                         font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50")
        titulo.pack(pady=20)
        
        # Frame principal para os botões
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        # Botões das funcionalidades
        self.criar_botao_funcionalidade(frame_botoes, "📋 1. Consultar Acordo", 
                                       "Consulta status de acordos usando cod_cliente e cod_acordo",
                                       self.abrir_consultar_acordo, row=0, col=0)
        
        self.criar_botao_funcionalidade(frame_botoes, "🔍 2. Obter Dívida por CPF", 
                                       "Obtém informações de dívida ativa por CPF",
                                       self.abrir_obter_divida, row=0, col=1)
        
        self.criar_botao_funcionalidade(frame_botoes, "📄 3. Extrair JSON", 
                                       "Extrai dados de corpo_requisicao em formato JSON",
                                       self.abrir_extrair_json, row=1, col=0)
        
        self.criar_botao_funcionalidade(frame_botoes, "📁 4. Converter CSV → XLSX", 
                                       "Converte arquivos CSV para formato Excel",
                                       self.abrir_conversor, row=1, col=1)
        
        # Separador
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=20)
        
        # Frame de progresso (inicialmente oculto)
        self.frame_progresso = tk.Frame(self.root, bg="#f0f0f0")
        
        # Barra de progresso
        self.progresso_bar = ttk.Progressbar(self.frame_progresso, variable=self.progresso_var, 
                                           maximum=100, length=600)
        self.progresso_bar.pack(pady=10)
        
        # Labels de status
        self.label_progresso = tk.Label(self.frame_progresso, text="0/0", 
                                       font=("Arial", 10), bg="#f0f0f0")
        self.label_progresso.pack()
        
        self.label_status = tk.Label(self.frame_progresso, text="Pronto", 
                                    font=("Arial", 10), bg="#f0f0f0", fg="#27ae60")
        self.label_status.pack(pady=5)
        
        # Botões de controle (inicialmente ocultos)
        self.frame_controles = tk.Frame(self.frame_progresso, bg="#f0f0f0")
        self.frame_controles.pack(pady=10)
        
        self.btn_parar = tk.Button(self.frame_controles, text="⏸️ Parar", 
                                  command=self.parar_processo, state="disabled",
                                  bg="#f39c12", fg="white", font=("Arial", 10, "bold"))
        self.btn_parar.pack(side="left", padx=5)
        
        self.btn_cancelar = tk.Button(self.frame_controles, text="❌ Cancelar", 
                                     command=self.cancelar_processo, state="disabled",
                                     bg="#e74c3c", fg="white", font=("Arial", 10, "bold"))
        self.btn_cancelar.pack(side="left", padx=5)
        
        self.btn_voltar = tk.Button(self.frame_controles, text="🔙 Voltar ao Menu", 
                                   command=self.voltar_menu,
                                   bg="#95a5a6", fg="white", font=("Arial", 10, "bold"))
        self.btn_voltar.pack(side="left", padx=5)
    
    def criar_botao_funcionalidade(self, parent, titulo, descricao, comando, row, col):
        frame = tk.Frame(parent, bg="#ecf0f1", relief="raised", bd=2, padx=20, pady=15)
        frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configurar grid weight
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Título do botão
        btn_titulo = tk.Button(frame, text=titulo, command=comando,
                              font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                              padx=20, pady=10, cursor="hand2")
        btn_titulo.pack(fill="x", pady=(0, 10))
        
        # Descrição
        lbl_desc = tk.Label(frame, text=descricao, font=("Arial", 9), 
                           bg="#ecf0f1", fg="#7f8c8d", wraplength=200, justify="center")
        lbl_desc.pack()
    
    def mostrar_progresso(self):
        """Mostra a área de progresso e oculta os botões principais"""
        self.frame_progresso.pack(fill="x", padx=20, pady=20)
        
    def ocultar_progresso(self):
        """Oculta a área de progresso"""
        self.frame_progresso.pack_forget()
        
    def voltar_menu(self):
        """Volta para o menu principal"""
        self.parar_flag.set()
        self.cancelar_flag.set()
        self.ocultar_progresso()
        self.resetar_controles()
        
    def resetar_controles(self):
        """Reseta os controles para o estado inicial"""
        self.progresso_var.set(0)
        self.label_progresso.config(text="0/0")
        self.label_status.config(text="Pronto", fg="#27ae60")
        self.btn_parar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.parar_flag.clear()
        self.cancelar_flag.clear()
        
    def parar_processo(self):
        """Para o processo atual salvando o progresso"""
        self.parar_flag.set()
        self.label_status.config(text="⏸️ Parando processo...", fg="#f39c12")
        self.btn_parar.config(state="disabled")
        
    def cancelar_processo(self):
        """Cancela o processo atual sem salvar"""
        self.cancelar_flag.set()
        self.parar_flag.set()
        self.label_status.config(text="❌ Cancelando processo...", fg="#e74c3c")
        self.btn_parar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
    
    # === FUNCIONALIDADE 1: CONSULTAR ACORDO ===
    def abrir_consultar_acordo(self):
        """Abre a funcionalidade de consultar acordo"""
        self.mostrar_progresso()
        self.label_status.config(text="🔧 Preparando Consultar Acordo...", fg="#3498db")
        
        # Gerar modelo
        if self.gerar_modelo_consultar_acordo():
            # Solicitar arquivo de entrada
            self.processar_consultar_acordo()
    
    def gerar_modelo_consultar_acordo(self):
        """Gera o modelo XLSX para consultar acordo"""
        try:
            # Dados do modelo
            modelo_data = {
                'cod_cliente': [12345, 67890, 54321],
                'cod_acordo': [98765, 43210, 11111],
                'status_acordo': ['', '', '']  # Será preenchido pelo processo
            }
            
            df_modelo = pd.DataFrame(modelo_data)
            
            # Escolher onde salvar o modelo
            arquivo_modelo = filedialog.asksaveasfilename(
                title="📋 Salvar modelo para Consultar Acordo",
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                initialfile="modelo_consultar_acordo.xlsx"
            )
            
            if not arquivo_modelo:
                self.voltar_menu()
                return False
            
            # Salvar modelo
            df_modelo.to_excel(arquivo_modelo, index=False)
            
            self.label_status.config(text=f"✅ Modelo salvo: {os.path.basename(arquivo_modelo)}", fg="#27ae60")
            messagebox.showinfo("Modelo Criado", 
                              f"Modelo salvo com sucesso!\n\n"
                              f"Arquivo: {arquivo_modelo}\n\n"
                              f"Preencha as colunas 'cod_cliente' e 'cod_acordo' e execute novamente.\n"
                              f"A coluna 'status_acordo' será preenchida automaticamente.")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar modelo: {str(e)}")
            self.voltar_menu()
            return False
    
    def processar_consultar_acordo(self):
        """Processa a consulta de acordo"""
        # Solicitar arquivo preenchido
        arquivo_entrada = filedialog.askopenfilename(
            title="📂 Selecionar arquivo preenchido para processar",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if not arquivo_entrada:
            self.voltar_menu()
            return
            
        # Escolher onde salvar resultado
        arquivo_saida = filedialog.asksaveasfilename(
            title="💾 Salvar resultado processado",
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile="resultado_consultar_acordo.xlsx"
        )
        
        if not arquivo_saida:
            self.voltar_menu()
            return
        
        # Iniciar processamento em thread separada
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        thread = threading.Thread(target=self._processar_consultar_acordo_thread,
                                args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()
    
    def _processar_consultar_acordo_thread(self, arquivo_entrada, arquivo_saida):
        """Thread para processar consulta de acordo"""
        try:
            df = pd.read_excel(arquivo_entrada)
            
            if 'cod_cliente' not in df.columns or 'cod_acordo' not in df.columns:
                messagebox.showerror("Erro", "Arquivo deve conter as colunas 'cod_cliente' e 'cod_acordo'")
                self.voltar_menu()
                return
            
            if 'status_acordo' not in df.columns:
                df['status_acordo'] = ''
            
            total = len(df)
            processados = 0
            
            for i, row in df.iterrows():
                if self.parar_flag.is_set() or self.cancelar_flag.is_set():
                    break
                
                # Atualizar interface
                self.root.after(0, lambda: self.label_progresso.config(text=f"{processados}/{total}"))
                self.root.after(0, lambda: self.progresso_var.set(int((processados / total) * 100) if total > 0 else 0))
                self.root.after(0, lambda: self.label_status.config(text=f"🔍 Processando linha {processados + 1}...", fg="#3498db"))
                
                # Processar consulta
                status = self.consultar_status_acordo(row, i)
                df.at[i, 'status_acordo'] = status
                
                processados += 1
                
                # Salvar progresso a cada 10 linhas
                if processados % 10 == 0:
                    df.to_excel(arquivo_saida, index=False)
            
            # Salvar resultado final
            df.to_excel(arquivo_saida, index=False)
            
            if self.cancelar_flag.is_set():
                self.root.after(0, lambda: self.label_status.config(text="❌ Processo cancelado", fg="#e74c3c"))
            else:
                self.root.after(0, lambda: self.label_status.config(text="✅ Consulta de acordo concluída!", fg="#27ae60"))
                self.root.after(0, lambda: messagebox.showinfo("Concluído", f"Processo finalizado!\nResultado salvo em: {arquivo_saida}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro no processamento: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.resetar_controles())
    
    def consultar_status_acordo(self, row, index, tentativas=2):
        """Consulta o status do acordo (mesmo código do arquivo original)"""
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
                response = requests.post(URL, data=payload, timeout=15)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "xml")
                string_tag = soup.find("string")

                if not string_tag:
                    raise ValueError("⚠️ Tag <string> não encontrada.")

                decoded = string_tag.text.replace("&lt;", "<").replace("&gt;", ">")
                status_match = re.search(r"<Status>(.*?)</Status>", decoded)

                if status_match:
                    return status_match.group(1)
                else:
                    raise ValueError("⚠️ Campo <Status> não encontrado.")

            except Exception:
                continue

        return "Não encontrado"
    
    # === FUNCIONALIDADE 2: OBTER DÍVIDA POR CPF ===
    def abrir_obter_divida(self):
        """Abre a funcionalidade de obter dívida por CPF"""
        self.mostrar_progresso()
        self.label_status.config(text="🔧 Preparando Obter Dívida por CPF...", fg="#3498db")
        
        if self.gerar_modelo_obter_divida():
            self.processar_obter_divida()
    
    def gerar_modelo_obter_divida(self):
        """Gera o modelo XLSX para obter dívida por CPF"""
        try:
            modelo_data = {
                'cpf': ['12345678901', '98765432100', '11122233344'],
                'cod_cliente': ['0', '0', '0'],
                'cod_acordo': ['0', '0', '0'],
                'status': ['', '', ''],
                'observacao': ['', '', ''],
                'data_vencimento': ['', '', '']
            }
            
            df_modelo = pd.DataFrame(modelo_data)
            
            arquivo_modelo = filedialog.asksaveasfilename(
                title="🔍 Salvar modelo para Obter Dívida por CPF",
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                initialfile="modelo_obter_divida.xlsx"
            )
            
            if not arquivo_modelo:
                self.voltar_menu()
                return False
            
            df_modelo.to_excel(arquivo_modelo, index=False)
            
            self.label_status.config(text=f"✅ Modelo salvo: {os.path.basename(arquivo_modelo)}", fg="#27ae60")
            messagebox.showinfo("Modelo Criado", 
                              f"Modelo salvo com sucesso!\n\n"
                              f"Arquivo: {arquivo_modelo}\n\n"
                              f"Preencha a coluna 'cpf' e execute novamente.\n"
                              f"As demais colunas serão preenchidas automaticamente.")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar modelo: {str(e)}")
            self.voltar_menu()
            return False
    
    def processar_obter_divida(self):
        """Processa obtenção de dívida por CPF"""
        arquivo_entrada = filedialog.askopenfilename(
            title="📂 Selecionar arquivo preenchido para processar",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if not arquivo_entrada:
            self.voltar_menu()
            return
            
        arquivo_saida = filedialog.asksaveasfilename(
            title="💾 Salvar resultado processado",
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile="resultado_obter_divida.xlsx"
        )
        
        if not arquivo_saida:
            self.voltar_menu()
            return
        
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        thread = threading.Thread(target=self._processar_obter_divida_thread,
                                args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()
    
    def _processar_obter_divida_thread(self, arquivo_entrada, arquivo_saida):
        """Thread para processar obtenção de dívida"""
        try:
            df = pd.read_excel(arquivo_entrada, dtype=str)
            df.columns = df.columns.str.strip().str.lower()
            
            if 'cpf' not in df.columns:
                messagebox.showerror("Erro", "Arquivo deve conter a coluna 'cpf'")
                self.voltar_menu()
                return
            
            # Garantir que as colunas existam
            for col in ['cod_cliente', 'cod_acordo', 'status', 'observacao']:
                if col not in df.columns:
                    df[col] = ''
            
            df.fillna("0", inplace=True)
            total = len(df)
            
            for i, row in df.iterrows():
                if self.parar_flag.is_set() or self.cancelar_flag.is_set():
                    break
                
                self.root.after(0, lambda i=i: self.label_progresso.config(text=f"{i}/{total}"))
                self.root.after(0, lambda i=i: self.progresso_var.set(int((i / total) * 100) if total > 0 else 0))
                self.root.after(0, lambda i=i: self.label_status.config(text=f"🔍 Processando CPF {i + 1}...", fg="#3498db"))
                
                # Processar CPF
                cpf = self.limpar_cpf(row.get('cpf', ''))
                if cpf and cpf != '00000000000':
                    id_cliente, id_acordo, _ = self.consultar_easycollector(cpf)
                    
                    if id_cliente != 0:
                        df.at[i, 'cod_cliente'] = str(id_cliente)
                    if id_acordo != 0:
                        df.at[i, 'cod_acordo'] = str(id_acordo)
                    
                    if id_cliente != 0 or id_acordo != 0:
                        df.at[i, 'status'] = 'Encontrado'
                        df.at[i, 'observacao'] = 'Encontrado com sucesso'
                    else:
                        df.at[i, 'status'] = 'Investigar'
                        df.at[i, 'observacao'] = 'Não encontrado'
                
                # Salvar a cada 10 linhas
                if i % 10 == 0:
                    df.to_excel(arquivo_saida, index=False)
            
            df.to_excel(arquivo_saida, index=False)
            
            if self.cancelar_flag.is_set():
                self.root.after(0, lambda: self.label_status.config(text="❌ Processo cancelado", fg="#e74c3c"))
            else:
                self.root.after(0, lambda: self.label_status.config(text="✅ Obtenção de dívida concluída!", fg="#27ae60"))
                self.root.after(0, lambda: messagebox.showinfo("Concluído", f"Processo finalizado!\nResultado salvo em: {arquivo_saida}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro no processamento: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.resetar_controles())
    
    def limpar_cpf(self, cpf_raw):
        """Limpa e formata CPF"""
        if not isinstance(cpf_raw, str):
            cpf_raw = str(cpf_raw)
        cpf_limpo = re.sub(r'\D', '', cpf_raw)
        return cpf_limpo.zfill(11) if cpf_limpo else ""
    
    def consultar_easycollector(self, cpf):
        """Consulta informações no EasyCollector"""
        payload = {
            "logonUsuario": LOGIN,
            "senhaUsuario": SENHA,
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
            print(f"Erro consultar_easycollector CPF {cpf}: {e}")
            return 0, 0, []
    
    # === FUNCIONALIDADE 3: EXTRAIR JSON ===
    def abrir_extrair_json(self):
        """Abre a funcionalidade de extrair JSON"""
        self.mostrar_progresso()
        self.label_status.config(text="🔧 Preparando Extrair JSON...", fg="#3498db")
        
        if self.gerar_modelo_extrair_json():
            self.processar_extrair_json()
    
    def gerar_modelo_extrair_json(self):
        """Gera o modelo XLSX para extrair JSON"""
        try:
            # Exemplo de JSON para o modelo
            exemplo_json = {
                "carga": {
                    "idCarga": 12345,
                    "origem": "CGFF001",
                    "nmArquivo": "exemplo.txt"
                },
                "clientesArquivo": [
                    {"nmArquivo": "cliente1.txt"}
                ]
            }
            
            modelo_data = {
                'corpo_requisicao': [
                    json.dumps(exemplo_json),
                    json.dumps(exemplo_json),
                    json.dumps(exemplo_json)
                ],
                'data_hora': [
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            
            df_modelo = pd.DataFrame(modelo_data)
            
            arquivo_modelo = filedialog.asksaveasfilename(
                title="📄 Salvar modelo para Extrair JSON",
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                initialfile="modelo_extrair_json.xlsx"
            )
            
            if not arquivo_modelo:
                self.voltar_menu()
                return False
            
            df_modelo.to_excel(arquivo_modelo, index=False)
            
            self.label_status.config(text=f"✅ Modelo salvo: {os.path.basename(arquivo_modelo)}", fg="#27ae60")
            messagebox.showinfo("Modelo Criado", 
                              f"Modelo salvo com sucesso!\n\n"
                              f"Arquivo: {arquivo_modelo}\n\n"
                              f"Preencha a coluna 'corpo_requisicao' com dados JSON e execute novamente.\n"
                              f"Os dados serão extraídos automaticamente.")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar modelo: {str(e)}")
            self.voltar_menu()
            return False
    
    def processar_extrair_json(self):
        """Processa extração de JSON"""
        arquivo_entrada = filedialog.askopenfilename(
            title="📂 Selecionar arquivo preenchido para processar",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if not arquivo_entrada:
            self.voltar_menu()
            return
            
        arquivo_saida = filedialog.asksaveasfilename(
            title="💾 Salvar resultado processado",
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile="resultado_extrair_json.xlsx"
        )
        
        if not arquivo_saida:
            self.voltar_menu()
            return
        
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        thread = threading.Thread(target=self._processar_extrair_json_thread,
                                args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()
    
    def _processar_extrair_json_thread(self, arquivo_entrada, arquivo_saida):
        """Thread para processar extração de JSON"""
        try:
            df = pd.read_excel(arquivo_entrada)
            
            if 'corpo_requisicao' not in df.columns:
                messagebox.showerror("Erro", "Arquivo deve conter a coluna 'corpo_requisicao'")
                self.voltar_menu()
                return
            
            total = len(df)
            registros = []
            
            for index, linha in df.iterrows():
                if self.parar_flag.is_set() or self.cancelar_flag.is_set():
                    break
                
                self.root.after(0, lambda i=index: self.label_progresso.config(text=f"{i}/{total}"))
                self.root.after(0, lambda i=index: self.progresso_var.set(int((i / total) * 100) if total > 0 else 0))
                self.root.after(0, lambda i=index: self.label_status.config(text=f"📄 Extraindo JSON {i + 1}...", fg="#3498db"))
                
                corpo = linha['corpo_requisicao']
                try:
                    if isinstance(corpo, str):
                        corpo_json = json.loads(corpo)
                        
                        carga = corpo_json.get("carga", {})
                        idCarga = carga.get('idCarga')
                        
                        if idCarga is not None:
                            origem = carga.get('origem')
                            if isinstance(origem, str) and origem.startswith("CGFF"):
                                origem = origem[4:]
                            
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
                                'data_hora': linha.get('data_hora')
                            })
                
                except Exception as e:
                    print(f"Erro na linha {index+1}: {e}")
            
            # Criar DataFrame resultado
            df_resultado = pd.DataFrame(registros)
            df_resultado.to_excel(arquivo_saida, index=False)
            
            if self.cancelar_flag.is_set():
                self.root.after(0, lambda: self.label_status.config(text="❌ Processo cancelado", fg="#e74c3c"))
            else:
                self.root.after(0, lambda: self.label_status.config(text="✅ Extração de JSON concluída!", fg="#27ae60"))
                self.root.after(0, lambda: messagebox.showinfo("Concluído", f"Processo finalizado!\nResultado salvo em: {arquivo_saida}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro no processamento: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.resetar_controles())
    
    # === FUNCIONALIDADE 4: CONVERSOR CSV → XLSX ===
    def abrir_conversor(self):
        """Abre a funcionalidade de conversor CSV para XLSX"""
        self.mostrar_progresso()
        self.label_status.config(text="🔧 Preparando Conversor CSV → XLSX...", fg="#3498db")
        
        messagebox.showinfo("Conversor CSV → XLSX", 
                          "Esta ferramenta converte arquivos CSV para XLSX.\n\n"
                          "Selecione os arquivos CSV que deseja converter.")
        
        self.processar_conversor()
    
    def processar_conversor(self):
        """Processa a conversão de CSV para XLSX"""
        # Selecionar arquivos CSV
        arquivos_csv = filedialog.askopenfilenames(
            title="📁 Selecionar arquivos CSV para converter",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if not arquivos_csv:
            self.voltar_menu()
            return
        
        # Escolher pasta de destino
        pasta_destino = filedialog.askdirectory(
            title="📂 Escolher pasta para salvar arquivos XLSX"
        )
        
        if not pasta_destino:
            self.voltar_menu()
            return
        
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        thread = threading.Thread(target=self._processar_conversor_thread,
                                args=(arquivos_csv, pasta_destino))
        thread.daemon = True
        thread.start()
    
    def _processar_conversor_thread(self, arquivos_csv, pasta_destino):
        """Thread para processar conversão de CSV"""
        try:
            total = len(arquivos_csv)
            convertidos = 0
            erros = []
            
            for i, arquivo_csv in enumerate(arquivos_csv):
                if self.parar_flag.is_set() or self.cancelar_flag.is_set():
                    break
                
                self.root.after(0, lambda i=i: self.label_progresso.config(text=f"{i}/{total}"))
                self.root.after(0, lambda i=i: self.progresso_var.set(int((i / total) * 100) if total > 0 else 0))
                self.root.after(0, lambda nome=os.path.basename(arquivo_csv): 
                              self.label_status.config(text=f"📁 Convertendo {nome}...", fg="#3498db"))
                
                try:
                    # Detectar delimitador
                    delimitador = self.detectar_delimitador(arquivo_csv)
                    
                    # Ler CSV
                    df = pd.read_csv(arquivo_csv, delimiter=delimitador)
                    
                    # Corrigir cabeçalhos
                    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", '')
                    
                    # Gerar nome do arquivo XLSX
                    nome_arquivo = os.path.splitext(os.path.basename(arquivo_csv))[0] + '.xlsx'
                    caminho_xlsx = os.path.join(pasta_destino, nome_arquivo)
                    
                    # Salvar como XLSX
                    df.to_excel(caminho_xlsx, index=False)
                    convertidos += 1
                    
                except Exception as e:
                    erros.append(f"{os.path.basename(arquivo_csv)}: {str(e)}")
            
            # Salvar log de erros se houver
            if erros:
                nome_log = os.path.join(pasta_destino, "log_conversao.txt")
                with open(nome_log, "w", encoding="utf-8") as f:
                    f.write(f"[LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
                    for erro in erros:
                        f.write(f"{erro}\n")
            
            if self.cancelar_flag.is_set():
                self.root.after(0, lambda: self.label_status.config(text="❌ Processo cancelado", fg="#e74c3c"))
            else:
                self.root.after(0, lambda: self.label_status.config(text="✅ Conversão concluída!", fg="#27ae60"))
                msg = f"Conversão finalizada!\n\nConvertidos: {convertidos}/{total}"
                if erros:
                    msg += f"\nErros: {len(erros)} (ver log_conversao.txt)"
                self.root.after(0, lambda: messagebox.showinfo("Concluído", msg))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro no processamento: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.resetar_controles())
    
    def detectar_delimitador(self, caminho):
        """Detecta o delimitador do arquivo CSV"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                primeira_linha = f.readline()
                if ';' in primeira_linha:
                    return ';'
                elif ',' in primeira_linha:
                    return ','
                elif '\t' in primeira_linha:
                    return '\t'
                else:
                    return ','
        except:
            return ','

def main():
    root = tk.Tk()
    app = Python4WorkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
