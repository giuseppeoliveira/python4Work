"""
PYTHON4WORK PROFESSIONAL - Interface Unificada Avançada
Versão profissional com logging, validação, temas e configurações avançadas.

Características Profissionais:
- Sistema de logging estruturado
- Validação robusta de dados
- Temas visuais personalizáveis
- Configurações avançadas
- Relatórios detalhados
- Sistema de backup automático
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import json
from datetime import datetime, timedelta
import threading
import time
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
from dotenv import load_dotenv
import uuid
from pathlib import Path
import sys

# Adicionar o diretório raiz do projeto ao sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importar sistemas profissionais
from core.config_manager import ConfigManager
from core.professional_logger import LoggerProfissional
from core.data_validator import ValidadorDados
from core.theme_manager import GerenciadorTema

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações globais
LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")
URL = os.getenv("URL")
URL_DIVIDA = os.getenv("URL_DIVIDA")

class Python4WorkPro:
    def __init__(self, root):
        self.root = root
        self.session_id = str(uuid.uuid4())[:8]
        
        # Inicializar sistemas profissionais
        self.config = ConfigManager()
        self.logger = LoggerProfissional("Python4WorkPro", self.config)
        self.validator = ValidadorDados(self.logger)
        self.theme_manager = GerenciadorTema()

        # Iniciar sessão de logging
        self.session_logger = self.logger.create_session_log(self.session_id)

        # Configurar tema
        # Forçar tema corporativo para a interface profissional (identidade visual)
        self.theme_manager.set_theme('corporate')

        # Variáveis de controle
        self.progresso_var = tk.IntVar()
        self.parar_flag = threading.Event()
        self.cancelar_flag = threading.Event()
        self.current_operation = None
        self.backup_counter = 0
        
        # Configurar janela principal
        self.configurar_janela()
        self.criar_interface_profissional()
        
        # Log início da aplicação
        self.logger.log_user_action("Aplicação iniciada", session_id=self.session_id, theme=self.config.get('app.theme'))
    
    def configurar_janela(self):
        """Configura a janela principal com tema profissional"""
        # Configurações da janela
        width = self.config.get('ui.window_width', 1000)
        height = self.config.get('ui.window_height', 700)
        
        self.root.title(f"{self.config.get('app.name', 'Python4Work Professional')} v{self.config.get('app.version', '2.0.0')}")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(800, 600)
        
        # Aplicar tema
        self.theme_manager.create_themed_window(self.root)
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configurar fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_nolog_popup(self, title: str, geometry: str = "500x400"):
        """Cria um popup estilizado usando as cores/fontes do Manter Sessão para consistência."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(geometry)
        popup.transient(self.root)
        try:
            popup.grab_set()
        except Exception:
            pass

    # Paleta Manter Sessão
        popup._nolog_bg = "#2c3e50"
        popup._nolog_surface = "#34495e"
        popup._nolog_text = "#ecf0f1"
        popup._nolog_muted = "#95a5a6"
        popup._nolog_font = ("Segoe UI", 10)

        popup.configure(bg=popup._nolog_bg)
        return popup
    
    def criar_interface_profissional(self):
        """Cria interface profissional com layout moderno"""
        # Frame principal com scroll
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
    # Header removed for a compact layout (keeps only direct modules)
        
        # Cards das funcionalidades
        self.criar_cards_funcionalidades()
        
        # Área de progresso (inicialmente oculta)
        self.criar_area_progresso()
        
        # Footer com informações de status
        self.criar_footer()
        
        # Configurar grid
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind scroll do mouse
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def criar_header(self):
        # Header removed to keep a compact single-screen layout
        # Kept minimal to avoid syntax errors when header is intentionally omitted.
        pass
    
    def criar_cards_funcionalidades(self):
        """Cria cards das funcionalidades com design profissional e responsivo"""
        # Container dos cards
        cards_container = tk.Frame(self.scrollable_frame, bg=self.theme_manager.get_color('background'))
        cards_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Configurar grid responsivo - 2 colunas em telas normais, 1 em telas pequenas
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)
        cards_container.grid_rowconfigure(2, weight=1)
        cards_container.grid_columnconfigure(0, weight=1, minsize=300)  # Largura mínima
        cards_container.grid_columnconfigure(1, weight=1, minsize=300)  # Largura mínima
        
        # Definição dos cards
        funcionalidades = [
            {
                'titulo': '📋 Consultar Acordo',
                'descricao': 'Consulta status de acordos usando códigos de cliente e acordo',
                'icone': '📋',
                'cor': 'primary',
                'comando': self.abrir_consultar_acordo,
                'row': 0, 'col': 0
            },
            {
                'titulo': '🔍 Obter Dívida por CPF',
                'descricao': 'Obtém informações de dívida ativa consultando por CPF',
                'icone': '🔍',
                'cor': 'success',
                'comando': self.abrir_obter_divida,
                'row': 0, 'col': 1
            },
            {
                'titulo': '📄 Extrair JSON',
                'descricao': 'Extrai e estrutura dados de campos JSON complexos',
                'icone': '📄',
                'cor': 'warning',
                'comando': self.abrir_extrair_json,
                'row': 1, 'col': 0
            },
            {
                'titulo': '📁 Converter CSV → XLSX',
                'descricao': 'Converte arquivos CSV para formato Excel com validação',
                'icone': '📁',
                'cor': 'accent',
                'comando': self.abrir_conversor,
                'row': 1, 'col': 1
            },
            {
                'titulo': '🎯 Resolver Duplicatas',
                'descricao': 'Resolve duplicatas com regras inteligentes: data_pagamento, cod_acordo e cod_prestacao',
                'icone': '🎯',
                'cor': 'primary',
                'comando': self.abrir_filtrar_duplicatas,
                'row': 2, 'col': 0
            },
            {
                'titulo': '🛡️ Manter Sessão',
                'descricao': 'Mantém sua sessão ativa impedindo bloqueio de tela e timeout',
                'icone': '🛡️',
                'cor': 'success',
                'comando': self.abrir_nolog,
                'row': 2, 'col': 1
            },
            {
                'titulo': '🔧 Separador de Dívidas',
                'descricao': 'Extrai e separa dívidas de XML do Easy Collector em JSON legível',
                'icone': '🔧',
                'cor': 'accent',
                'comando': self.abrir_separador_dividas,
                'row': 3, 'col': 0
            }
            ,
            {
                'titulo': '📆 Consulta Boleto Mensal',
                'descricao': 'Consulta dívidas por CPF e filtra por mês/ano (gera Excel consolidado)',
                'icone': '📆',
                'cor': 'primary',
                'comando': self.abrir_consulta_boleto_mensal,
                'row': 3, 'col': 1
            }
        ]
        
        # Criar cada card
        for func in funcionalidades:
            self.criar_card_funcionalidade(cards_container, func)
    
    def criar_card_funcionalidade(self, parent, config):
        """Cria um card individual de funcionalidade responsivo"""
        # Frame do card
        card = self.theme_manager.create_card_frame(parent)
        card.grid(row=config['row'], column=config['col'], 
                 padx=10, pady=10, sticky="nsew")
        
        # Container interno com padding reduzido para economizar espaço
        card_content = tk.Frame(card, bg=self.theme_manager.get_color('surface'))
        card_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header com ícone e título em linha (mais compacto)
        header_frame = tk.Frame(card_content, bg=self.theme_manager.get_color('surface'))
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Ícone médio
        icon_label = tk.Label(header_frame, text=config['icone'], 
                             font=("Arial", 24), bg=self.theme_manager.get_color('surface'))
        icon_label.pack(side='left', padx=(0, 10))
        
        # Título ao lado do ícone
        title_label = tk.Label(header_frame, text=config['titulo'], 
                              font=("Arial", 12, "bold"), anchor='w')
        self.theme_manager.apply_theme_to_widget(title_label, 'subtitle')
        title_label.pack(side='left', fill='x', expand=True)
        
        # Descrição compacta
        desc_label = tk.Label(card_content, text=config['descricao'], 
                             font=("Arial", 9), wraplength=250, justify='left',
                             anchor='w')
        self.theme_manager.apply_theme_to_widget(desc_label, 'description')
        desc_label.pack(fill='x', pady=(0, 15))
        
        # Botão principal menor
        btn = tk.Button(card_content, text="▶ Iniciar", 
                       command=config['comando'],
                       font=("Arial", 10, "bold"), padx=15, pady=6)
        self.theme_manager.apply_theme_to_widget(btn, f"{config['cor']}_button")
        btn.pack(anchor='w')
        
        # Estatísticas compactas
        stats_frame = tk.Frame(card_content, bg=self.theme_manager.get_color('surface'))
        stats_frame.pack(fill='x', pady=(10, 0))
        
        stats_label = tk.Label(stats_frame, text="📊 Pronto para uso", 
                              font=("Arial", 8), anchor='w')
        self.theme_manager.apply_theme_to_widget(stats_label, 'description')
        stats_label.pack(anchor='w')
    
    def criar_area_progresso(self):
        """Cria área de progresso profissional"""
        self.frame_progresso = self.theme_manager.create_card_frame(self.scrollable_frame, "📊 Progresso da Operação")
        
        # Container interno
        progress_content = tk.Frame(self.frame_progresso, bg=self.theme_manager.get_color('surface'))
        progress_content.pack(fill='x', padx=20, pady=20)
        
        # Nome da operação atual
        self.label_operacao = tk.Label(progress_content, text="Nenhuma operação em andamento", 
                                      font=("Arial", 12, "bold"))
        self.theme_manager.apply_theme_to_widget(self.label_operacao, 'subtitle')
        self.label_operacao.pack(pady=(0, 15))
        
        # Barra de progresso principal
        self.progresso_bar = ttk.Progressbar(progress_content, variable=self.progresso_var, 
                                           maximum=100, length=600)
        self.progresso_bar.pack(pady=(0, 10))
        
        # Labels de progresso
        progress_info_frame = tk.Frame(progress_content, bg=self.theme_manager.get_color('surface'))
        progress_info_frame.pack(fill='x', pady=(0, 15))
        
        self.label_progresso = tk.Label(progress_info_frame, text="0/0 (0%)", 
                                      font=("Arial", 10, "bold"))
        self.theme_manager.apply_theme_to_widget(self.label_progresso, 'description')
        self.label_progresso.pack(side='left')
        
        self.label_tempo = tk.Label(progress_info_frame, text="Tempo: --", 
                                   font=("Arial", 10))
        self.theme_manager.apply_theme_to_widget(self.label_tempo, 'description')
        self.label_tempo.pack(side='right')
        
        # Status detalhado
        self.label_status = self.theme_manager.create_status_label(progress_content, "Pronto", "info")
        self.label_status.pack(pady=(0, 20))
        
        # Botões de controle
        controls_frame = tk.Frame(progress_content, bg=self.theme_manager.get_color('surface'))
        controls_frame.pack(fill='x')
        
        self.btn_parar = tk.Button(controls_frame, text="⏸️ Pausar", 
                                  command=self.parar_processo, state="disabled",
                                  font=("Arial", 10, "bold"), padx=15, pady=8)
        self.theme_manager.apply_theme_to_widget(self.btn_parar, 'warning_button')
        self.btn_parar.pack(side="left", padx=(0, 10))
        
        self.btn_cancelar = tk.Button(controls_frame, text="❌ Cancelar", 
                                     command=self.cancelar_processo, state="disabled",
                                     font=("Arial", 10, "bold"), padx=15, pady=8)
        self.theme_manager.apply_theme_to_widget(self.btn_cancelar, 'danger_button')
        self.btn_cancelar.pack(side="left", padx=(0, 10))
        
        self.btn_voltar = tk.Button(controls_frame, text="🔙 Voltar ao Menu", 
                                   command=self.voltar_menu,
                                   font=("Arial", 10, "bold"), padx=15, pady=8)
        self.theme_manager.apply_theme_to_widget(self.btn_voltar, 'secondary_button')
        self.btn_voltar.pack(side="right")
    
    def criar_footer(self):
        """Cria footer com informações do sistema"""
        footer_frame = tk.Frame(self.scrollable_frame, bg=self.theme_manager.get_color('light'), height=50)
        footer_frame.pack(fill='x', padx=20, pady=(10, 20))
        footer_frame.pack_propagate(False)
        
        # Informações do sistema
        system_info = f"💻 Python4Work Professional v{self.config.get('app.version', '2.0.0')} | 🛡️ Segurança: Ativa | 📝 Logs: Habilitados"
        footer_label = tk.Label(footer_frame, text=system_info, 
                               font=("Arial", 8), bg=self.theme_manager.get_color('light'))
        footer_label.pack(expand=True)
    
    def mostrar_progresso(self, operacao_nome: str):
        """Mostra área de progresso com nome da operação"""
        self.current_operation = operacao_nome
        self.label_operacao.config(text=f"🔄 {operacao_nome}")
        self.frame_progresso.pack(fill='x', padx=20, pady=10)
        
        # Scroll para a área de progresso
        self.root.update()
        self.scrollable_frame.update()
        
        self.logger.log_operation_start(operacao_nome, session_id=self.session_id)
        
        # --- Modal progress popup (modal) ---
        try:
            # Use centralized NoLogout-styled popup for modal progress
            self._modal_progress = self._create_nolog_popup("Processando...", geometry="400x120")
            try:
                self._modal_progress.resizable(False, False)
            except Exception:
                pass

            body = tk.Frame(self._modal_progress, bg=self.theme_manager.get_color('surface'))
            body.pack(fill='both', expand=True, padx=12, pady=12)

            lbl = tk.Label(body, text=f"{operacao_nome}", font=("Arial", 11, 'bold'), bg=self.theme_manager.get_color('surface'))
            self.theme_manager.apply_theme_to_widget(lbl, 'subtitle')
            lbl.pack(anchor='w', pady=(0, 8))

            self._modal_progress_bar = ttk.Progressbar(body, variable=self.progresso_var, maximum=100, length=340)
            self._modal_progress_bar.pack(pady=(4, 8))

            self._modal_progress_info = tk.Label(body, text="Aguardando...", bg=self.theme_manager.get_color('surface'))
            self.theme_manager.apply_theme_to_widget(self._modal_progress_info, 'description')
            self._modal_progress_info.pack(anchor='w')
        except Exception:
            # If modal creation fails for any reason, continue without modal
            self._modal_progress = None
    
    def atualizar_progresso(self, progresso, status="Processando..."):
        """Atualiza barra de progresso e status"""
        def _update():
            self.progresso_var.set(int(progresso))
            self.label_status.config(text=status)
            # Atualizar tempo estimado se necessário
            if hasattr(self, 'start_time'):
                elapsed = time.time() - self.start_time
                self.label_tempo.config(text=f"Tempo: {elapsed:.1f}s")
        
        # Executar na thread principal
        self.root.after(0, _update)
    
    def ocultar_progresso(self):
        """Oculta área de progresso"""
        self.frame_progresso.pack_forget()
        if self.current_operation:
            self.logger.log_operation_end(self.current_operation, session_id=self.session_id)
        self.current_operation = None
        # Destroy modal if present
        try:
            if hasattr(self, '_modal_progress') and self._modal_progress:
                try:
                    self._modal_progress.grab_release()
                except Exception:
                    pass
                try:
                    self._modal_progress.destroy()
                except Exception:
                    pass
                self._modal_progress = None
        except Exception:
            pass
    
    def voltar_menu(self):
        """Volta para o menu principal"""
        self.parar_flag.set()
        self.cancelar_flag.set()
        self.ocultar_progresso()
        self.resetar_controles()
        self.logger.log_user_action("Voltou ao menu principal", session_id=self.session_id)
    
    def resetar_controles(self):
        """Reseta controles para estado inicial"""
        self.progresso_var.set(0)
        self.label_progresso.config(text="0/0 (0%)")
        self.label_tempo.config(text="Tempo: --")
        self.label_status.config(text="Pronto")
        self.btn_parar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.parar_flag.clear()
        self.cancelar_flag.clear()
        self.backup_counter = 0
    
    def parar_processo(self):
        """Para processo salvando progresso"""
        self.parar_flag.set()
        self.label_status.config(text="⏸️ Pausando processo...")
        self.btn_parar.config(state="disabled")
        self.logger.log_user_action("Pausou processo", operation=self.current_operation, session_id=self.session_id)
    
    def cancelar_processo(self):
        """Cancela processo atual"""
        self.cancelar_flag.set()
        self.parar_flag.set()
        self.label_status.config(text="❌ Cancelando processo...")
        self.btn_parar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.logger.log_user_action("Cancelou processo", operation=self.current_operation, session_id=self.session_id)
    
    def verificar_conectividade(self):
        """Verifica conectividade com APIs"""
        try:
            if LOGIN and SENHA and URL:
                # Teste rápido de conectividade
                response = requests.get("http://54.83.29.48", timeout=5)
                self.root.after(0, lambda: self.status_connectivity.config(text="🟢 Conectado"))
                self.logger.info("Conectividade verificada", status="success")
            else:
                self.root.after(0, lambda: self.status_connectivity.config(text="🟡 Configuração incompleta"))
                self.logger.warning("Variáveis de ambiente incompletas")
        except:
            self.root.after(0, lambda: self.status_connectivity.config(text="🔴 Offline"))
            self.logger.warning("Falha na verificação de conectividade")
    
    def abrir_configuracoes(self):
        """Abre janela de configurações FUNCIONAL"""
        self.logger.log_user_action("Abriu configurações", session_id=self.session_id)
        
        # Criar janela de configurações usando popup centralizado
        config_window = self._create_nolog_popup("⚙️ Configurações", geometry="500x400")
        try:
            config_window.resizable(False, False)
        except Exception:
            pass

        # Aplicar tema
        config_window.configure(bg=self.theme_manager.get_color('background'))
        
        # Frame principal
        main_frame = tk.Frame(config_window, bg=self.theme_manager.get_color('background'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="⚙️ Configurações da Aplicação", 
                              font=("Arial", 14, "bold"))
        self.theme_manager.apply_theme_to_widget(title_label, 'title')
        title_label.pack(pady=(0, 20))
        
        # Theme selection removed — UI now uses a single corporate blue theme
        # to keep the professional appearance consistent. Theme is controlled
        # centrally by ThemeManager (default: 'corporate').
        
        # Configurações de logging
        log_frame = tk.LabelFrame(main_frame, text="📝 Sistema de Logging", 
                                 font=("Arial", 10, "bold"), padx=10, pady=10)
        self.theme_manager.apply_theme_to_widget(log_frame, 'surface')
        log_frame.pack(fill='x', pady=(0, 15))
        
        log_level_var = tk.StringVar(value=self.config.get('logging.level', 'INFO'))
        log_levels = [("🔍 DEBUG", "DEBUG"), ("ℹ️ INFO", "INFO"), ("⚠️ WARNING", "WARNING")]
        
        for text, value in log_levels:
            rb = tk.Radiobutton(log_frame, text=text, variable=log_level_var, value=value)
            self.theme_manager.apply_theme_to_widget(rb, 'surface')
            rb.pack(anchor='w')
        
        # Botões
        button_frame = tk.Frame(main_frame, bg=self.theme_manager.get_color('background'))
        button_frame.pack(fill='x', pady=(20, 0))
        
        def salvar_config():
            # Do not allow changing the theme from the UI; keep corporate theme.
            self.config.set('logging.level', log_level_var.get())
            messagebox.showinfo("Sucesso", "Configurações salvas!\nReinicie para aplicar todas as mudanças.")
            config_window.destroy()
        
        btn_salvar = tk.Button(button_frame, text="💾 Salvar", command=salvar_config,
                              font=("Arial", 10, "bold"), padx=20)
        self.theme_manager.apply_theme_to_widget(btn_salvar, 'primary_button')
        btn_salvar.pack(side='right', padx=(10, 0))
        
        btn_cancelar = tk.Button(button_frame, text="❌ Cancelar", 
                                command=config_window.destroy,
                                font=("Arial", 10, "bold"), padx=20)
        self.theme_manager.apply_theme_to_widget(btn_cancelar, 'secondary_button')
        btn_cancelar.pack(side='right')
    
    def aplicar_tema(self, tema):
        """Aplica tema imediatamente em toda a interface"""
        self.theme_manager.set_theme(tema)
        self.config.set('app.theme', tema)
        
        # Aplicar tema a toda a interface principal
        self.root.configure(bg=self.theme_manager.get_color('background'))
        
        # Atualizar todos os widgets principais
        try:
            # Reconfigurar scrollable_frame
            if hasattr(self, 'scrollable_frame'):
                self.scrollable_frame.configure(bg=self.theme_manager.get_color('background'))
            
            # Atualizar todos os widgets filhos recursivamente
            self._atualizar_tema_recursivo(self.root)
            
            # Salvar configuração
            self.logger.info(f"Tema alterado para: {tema}")
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar tema: {e}")
    
    def _atualizar_tema_recursivo(self, widget):
        """Atualiza tema recursivamente em todos os widgets"""
        try:
            # Aplicar cor de fundo padrão
            if widget.winfo_class() in ['Frame', 'Toplevel']:
                widget.configure(bg=self.theme_manager.get_color('background'))
            elif widget.winfo_class() == 'Canvas':
                widget.configure(bg=self.theme_manager.get_color('background'))
                
            # Processar todos os filhos
            for child in widget.winfo_children():
                self._atualizar_tema_recursivo(child)
                
        except Exception:
            pass  # Ignorar erros de widgets que não suportam configuração
        
    def abrir_relatorios(self):
        """Abre janela de relatórios FUNCIONAL"""
        self.logger.log_user_action("Abriu relatórios", session_id=self.session_id)
        
        # Criar janela de relatórios usando popup centralizado
        report_window = self._create_nolog_popup("📊 Relatórios e Logs", geometry="700x500")
        try:
            report_window.resizable(True, True)
        except Exception:
            pass

        # Aplicar tema
        report_window.configure(bg=self.theme_manager.get_color('background'))
        
        # Frame principal
        main_frame = tk.Frame(report_window, bg=self.theme_manager.get_color('background'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="📊 Relatórios do Sistema", 
                              font=("Arial", 14, "bold"))
        self.theme_manager.apply_theme_to_widget(title_label, 'title')
        title_label.pack(pady=(0, 20))
        
        # Notebook para abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Aba 1: Logs Recentes
        log_frame = tk.Frame(notebook, bg=self.theme_manager.get_color('surface'))
        notebook.add(log_frame, text="📝 Logs Recentes")
        
        log_text = tk.Text(log_frame, height=15, wrap='word')
        log_scroll = tk.Scrollbar(log_frame, orient="vertical", command=log_text.yview)
        log_text.configure(yscrollcommand=log_scroll.set)
        
        try:
            with open("logs/python4workpro.log", "r", encoding="utf-8") as f:
                logs = f.readlines()[-50:]  # Últimas 50 linhas
                log_text.insert(tk.END, "".join(logs))
        except:
            log_text.insert(tk.END, "Nenhum log encontrado.")
        
        log_text.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        log_scroll.pack(side='right', fill='y', pady=10, padx=(0, 10))
        
        # Aba 2: Estatísticas
        stats_frame = tk.Frame(notebook, bg=self.theme_manager.get_color('surface'))
        notebook.add(stats_frame, text="📈 Estatísticas")
        
        stats_text = tk.Text(stats_frame, height=15, wrap='word')
        
        # Gerar estatísticas básicas
        stats_info = f"""📊 ESTATÍSTICAS DO SISTEMA
        
🕐 Sessão Atual: {self.session_id}
📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🎨 Tema Ativo: {self.config.get('app.theme', 'modern')}
📝 Nível de Log: {self.config.get('logging.level', 'INFO')}

📁 ARQUIVOS DE LOG:
- Log Principal: logs/python4workpro.log
- Log de Erros: logs/python4workpro_errors.log
- Sessões: logs/sessions/

⚙️ CONFIGURAÇÕES:
- Auto Backup: {self.config.get('app.auto_backup', True)}
- Confirmar Saída: {self.config.get('ui.confirm_exit', True)}
- Tentativas Max: {self.config.get('app.max_retries', 3)}

🔧 SISTEMA:
- Python4Work Professional v{self.config.get('app.version', '2.0.0')}
- Interface: Profissional
- Status: Ativo ✅
"""
        
        stats_text.insert(tk.END, stats_info)
        stats_text.config(state='disabled')
        stats_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botões na janela
        button_frame = tk.Frame(main_frame, bg=self.theme_manager.get_color('background'))
        button_frame.pack(fill='x', pady=(10, 0))
        
        def abrir_pasta_logs():
            import subprocess
            subprocess.run(['explorer', os.path.abspath('logs')], shell=True)
        
        btn_logs = tk.Button(button_frame, text="📁 Abrir Pasta Logs", 
                            command=abrir_pasta_logs, font=("Arial", 10))
        self.theme_manager.apply_theme_to_widget(btn_logs, 'primary_button')
        btn_logs.pack(side='left')
        
        btn_fechar = tk.Button(button_frame, text="❌ Fechar", 
                              command=report_window.destroy, font=("Arial", 10))
        self.theme_manager.apply_theme_to_widget(btn_fechar, 'secondary_button')
        btn_fechar.pack(side='right')
    
    def on_closing(self):
        """Trata fechamento da aplicação"""
        if self.config.get('ui.confirm_exit', True):
            if messagebox.askyesno("Confirmar", "Deseja realmente sair?"):
                self.finalizar_aplicacao()
        else:
            self.finalizar_aplicacao()
    
    def finalizar_aplicacao(self):
        """Finaliza aplicação de forma limpa"""
        # Parar processos em andamento
        self.parar_flag.set()
        self.cancelar_flag.set()
        
        # Finalizar sessão de logging
        if hasattr(self, 'session_logger'):
            summary = {
                "operations_performed": bool(self.current_operation),
                "clean_exit": True
            }
            self.session_logger.finalize_session(summary)
        
        self.logger.log_user_action("Aplicação finalizada", session_id=self.session_id)
        
        # Salvar configurações se necessário
        self.config.save_config()
        
        # Fechar aplicação
        self.root.destroy()
    
    # === FUNCIONALIDADES IMPLEMENTADAS ===
    
    def abrir_consultar_acordo(self):
        """Funcionalidade consultar acordo com opção de baixar modelo"""
        self.mostrar_progresso("Consultar Acordo")
        self.logger.log_user_action("Iniciou Consultar Acordo", session_id=self.session_id)
        
        # Habilitar controles
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        # Janela de opções
        opcao = messagebox.askyesnocancel(
            "Consultar Acordo ⚡ OTIMIZADO",
            "Escolha uma opção:\n\n"
            "✅ SIM - Baixar modelo Excel primeiro\n"
            "❌ NÃO - Usar arquivo existente\n"
            "🚫 CANCELAR - Voltar ao menu\n\n"
            "⚡ Versão otimizada: 4-5x mais rápida!"
        )
        
        if opcao is None:  # Cancelar
            self.voltar_menu()
            return
        elif opcao:  # Baixar modelo
            self.baixar_modelo_consultar_acordo()
            return
        
        # Continuar com arquivo existente
        self.selecionar_arquivo_consultar_acordo()
    
    def baixar_modelo_consultar_acordo(self):
        """Baixa modelo Excel para consultar acordo"""
        import shutil
        
        arquivo_modelo = filedialog.asksaveasfilename(
            title="Salvar modelo Excel - Consultar Acordo",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="modelo_consultar_acordo.xlsx"
        )
        
        if not arquivo_modelo:
            self.voltar_menu()
            return
        
        try:
            # Copiar modelo da pasta Modelos
            modelo_origem = "Modelos/modelo_consultar_acordo.xlsx"
            
            if not os.path.exists(modelo_origem):
                messagebox.showerror("Erro", f"Modelo não encontrado: {modelo_origem}")
                self.voltar_menu()
                return
                
            shutil.copy2(modelo_origem, arquivo_modelo)
            
            messagebox.showinfo(
                "Modelo Copiado", 
                f"Modelo Excel copiado com sucesso!\n\n"
                f"📁 Arquivo: {arquivo_modelo}\n\n"
                f"📋 Colunas necessárias:\n"
                f"• cod_cliente (números)\n"
                f"• cod_acordo (números)\n"
                f"• observacoes (texto)\n\n"
                f"✅ Preencha os dados e execute novamente!"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar modelo: {e}")
        
        self.voltar_menu()
    
    def selecionar_arquivo_consultar_acordo(self):
        """Seleciona arquivo para consultar acordo"""
        # Seleção de arquivo
        arquivo_entrada = filedialog.askopenfilename(
            title="Selecione o arquivo Excel com cod_cliente e cod_acordo",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo_entrada:
            self.voltar_menu()
            return
        
        # Seleção de local para salvar
        arquivo_saida = filedialog.asksaveasfilename(
            title="Onde salvar o resultado?",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo_saida:
            self.voltar_menu()
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_consultar_acordo, 
                                args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()

    def abrir_consulta_boleto_mensal(self):
        """Abre interface para Consulta Boleto Mensal"""
        self.logger.log_user_action("Abriu Consulta Boleto Mensal", session_id=self.session_id)

        # Seleção de arquivo de entrada
        arquivo_entrada = filedialog.askopenfilename(
            title="Selecione o arquivo Excel com colunas: cod_aluno, cpf",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not arquivo_entrada:
            return

        # Perguntar ano e mês
        from tkinter import simpledialog
        ano = simpledialog.askinteger("Ano", "Informe o ano (AAAA):", parent=self.root, minvalue=2000, maxvalue=2100)
        if ano is None:
            return
        mes = simpledialog.askinteger("Mês", "Informe o mês (1-12):", parent=self.root, minvalue=1, maxvalue=12)
        if mes is None:
            return

        # Seleção de arquivo de saída
        arquivo_saida = filedialog.asksaveasfilename(
            title="Salvar resultado como",
            defaultextension=".xlsx",
            initialfile=f"consulta_boleto_{ano}{str(mes).zfill(2)}_{time.strftime('%Y%m%d_%H%M%S')}.xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not arquivo_saida:
            return

        # Inicializar barra de progresso e executar
        self.mostrar_progresso("Consulta Boleto Mensal")
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")

        thread = threading.Thread(target=self.executar_consulta_boleto_mensal,
                                  args=(arquivo_entrada, arquivo_saida, ano, mes))
        thread.daemon = True
        thread.start()

    def executar_consulta_boleto_mensal(self, arquivo_entrada, arquivo_saida, ano, mes):
        """Executa a consulta boleto mensal em background"""
        try:
            from src.consulta_boleto_mensal import run_consulta_boleto

            self.atualizar_progresso(5, "Iniciando consultas...")

            # run_consulta_boleto irá lançar exceção caso credenciais não existam
            df_result = run_consulta_boleto(arquivo_entrada, arquivo_saida, ano, mes)

            self.atualizar_progresso(100, "Consulta concluída")
            messagebox.showinfo("Sucesso", f"Consulta concluída. Arquivo gerado:\n{arquivo_saida}")

        except Exception as e:
            self.logger.error(f"Erro em Consulta Boleto Mensal: {e}")
            messagebox.showerror("Erro", f"Erro durante a consulta:\n{str(e)}")

        finally:
            self.voltar_menu()
    
    def executar_consultar_acordo(self, arquivo_entrada, arquivo_saida):
        """Executa consulta de acordo com validação robusta e processamento otimizado"""
        try:
            # Importar funções melhoradas do script
            from src.consultar_acordo import consultar_status_acordo_batch, validar_dados_entrada
            
            self.atualizar_progresso(5, f"📂 Carregando arquivo...")
            
            # Ler arquivo
            df = pd.read_excel(arquivo_entrada)
            total_linhas = len(df)
            
            self.logger.info(f"Consultar Acordo: Arquivo carregado - {total_linhas} registros")
            
            # Validar dados de entrada com nova função robusta
            self.atualizar_progresso(10, f"� Validando {total_linhas} registros...")
            
            try:
                registros_validos_esperados = validar_dados_entrada(df)
                self.logger.info(f"Consultar Acordo: Validação OK - {registros_validos_esperados} registros válidos esperados")
            except Exception as validation_error:
                error_msg = f"❌ Erro na validação: {validation_error}"
                self.logger.error(f"Consultar Acordo: {error_msg}")
                self.atualizar_progresso(0, error_msg)
                messagebox.showerror("Erro de Validação", str(validation_error))
                self.voltar_menu()
                return
            
            # Adicionar coluna de status se não existir
            if 'status_acordo' not in df.columns:
                df['status_acordo'] = ''
            
            self.atualizar_progresso(15, f"🚀 Iniciando consultas otimizadas...")
            
            # Configurações otimizadas
            batch_size = 50
            max_workers = 25
            linhas_processadas = 0
            
            import time
            start_time = time.time()
            
            # Processar em lotes para melhor performance
            for batch_start in range(0, total_linhas, batch_size):
                # Verificar flags de controle
                if self.cancelar_flag.is_set():
                    self.atualizar_progresso((batch_start/total_linhas)*100, "❌ Processo cancelado...")
                    break
                    
                if self.parar_flag.is_set():
                    self.atualizar_progresso((batch_start/total_linhas)*100, "⏸️ Processo pausado...")
                    self.parar_flag.wait()
                
                batch_end = min(batch_start + batch_size, total_linhas)
                batch_rows = [(i, df.iloc[i]) for i in range(batch_start, batch_end)]
                
                # Atualizar progresso
                progresso = int((batch_start / total_linhas) * 100)
                elapsed = time.time() - start_time
                if batch_start > 0:
                    eta = (elapsed / batch_start) * (total_linhas - batch_start)
                    self.atualizar_progresso(progresso, 
                        f"⚡ Processando lote {batch_start//batch_size + 1}: {batch_start+1}-{batch_end} de {total_linhas} | ETA: {eta/60:.1f}min")
                else:
                    self.atualizar_progresso(progresso, f"🔄 Processando lote 1: {batch_start+1}-{batch_end} de {total_linhas}")
                
                # Processar lote em paralelo
                batch_results = consultar_status_acordo_batch(batch_rows, max_workers)
                
                # Atualizar DataFrame com resultados
                for index, status in batch_results:
                    df.at[index, "status_acordo"] = status
                    linhas_processadas += 1
                
                # Salvar progresso periodicamente
                if linhas_processadas % 100 == 0:
                    df.to_excel(arquivo_saida, index=False)
            
            # Salvar arquivo final
            df.to_excel(arquivo_saida, index=False)
            
            # Calcular estatísticas finais
            total_time = time.time() - start_time
            req_per_sec = linhas_processadas / total_time if total_time > 0 else 0
            
            self.atualizar_progresso(100, 
                f"✅ Concluído! {linhas_processadas} registros em {total_time/60:.1f}min ({req_per_sec:.1f} req/s)")
            
            messagebox.showinfo("Sucesso", 
                f"Processamento concluído!\n\n"
                f"📊 Registros processados: {linhas_processadas}\n"
                f"⏱️ Tempo total: {total_time/60:.1f} minutos\n"
                f"⚡ Velocidade: {req_per_sec:.1f} req/s\n"
                f"📁 Arquivo salvo: {arquivo_saida}")
            
        except Exception as e:
            self.logger.critical(f"Erro crítico em consultar acordo: {e}")
            messagebox.showerror("Erro", f"Erro durante processamento: {str(e)}")
        finally:
            self.voltar_menu()
    
    def abrir_obter_divida(self):
        """Funcionalidade obter dívida com opção de baixar modelo"""
        self.mostrar_progresso("Obter Dívida por CPF")
        self.logger.log_user_action("Iniciou Obter Dívida", session_id=self.session_id)
        
        # Habilitar controles
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        # Janela de opções
        opcao = messagebox.askyesnocancel(
            "Obter Dívida por CPF",
            "Escolha uma opção:\n\n"
            "✅ SIM - Baixar modelo Excel primeiro\n"
            "❌ NÃO - Usar arquivo existente\n"
            "🚫 CANCELAR - Voltar ao menu"
        )
        
        if opcao is None:  # Cancelar
            self.voltar_menu()
            return
        elif opcao:  # Baixar modelo
            self.baixar_modelo_obter_divida()
            return
        
        # Continuar com arquivo existente
        self.selecionar_arquivo_obter_divida()
    
    def baixar_modelo_obter_divida(self):
        """Baixa modelo Excel para obter dívida por CPF"""
        import shutil
        
        arquivo_modelo = filedialog.asksaveasfilename(
            title="Salvar modelo Excel - Obter Dívida CPF",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="modelo_obter_divida_cpf.xlsx"
        )
        
        if not arquivo_modelo:
            self.voltar_menu()
            return
        
        try:
            # Copiar modelo da pasta Modelos
            modelo_origem = "Modelos/modelo_obter_divida_cpf.xlsx"
            
            if not os.path.exists(modelo_origem):
                messagebox.showerror("Erro", f"Modelo não encontrado: {modelo_origem}")
                self.voltar_menu()
                return
                
            shutil.copy2(modelo_origem, arquivo_modelo)
            
            messagebox.showinfo(
                "Modelo Copiado", 
                f"Modelo Excel copiado com sucesso!\n\n"
                f"📁 Arquivo: {arquivo_modelo}\n\n"
                f"📋 Colunas necessárias:\n"
                f"• cpf (11 dígitos)\n"
                f"• nome (texto)\n"
                f"• observacoes (texto)\n\n"
                f"✅ Preencha os dados e execute novamente!"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar modelo: {e}")
        
        self.voltar_menu()
    
    def selecionar_arquivo_obter_divida(self):
        """Seleciona arquivo para obter dívida"""
        # Seleção de arquivo
        arquivo_entrada = filedialog.askopenfilename(
            title="Selecione o arquivo Excel com CPFs",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo_entrada:
            self.voltar_menu()
            return
        
        # Seleção de local para salvar
        arquivo_saida = filedialog.asksaveasfilename(
            title="Onde salvar o resultado?",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo_saida:
            self.voltar_menu()
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_obter_divida, 
                                args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()
    
    def executar_obter_divida(self, arquivo_entrada, arquivo_saida):
        """Executa obtenção de dívida por CPF usando a função otimizada"""
        try:
            # Importar função otimizada
            from src.obter_divida_cpf import processar_batch_cpf
            import pandas as pd
            import time
            
            # Ler arquivo
            df = pd.read_excel(arquivo_entrada, engine='openpyxl', dtype=str)
            # Limpar nomes das colunas
            df.columns = df.columns.str.strip().str.lower()
            
            # Verificar se tem coluna CPF
            if "cpf" not in df.columns:
                messagebox.showerror("Erro", "Arquivo deve conter coluna 'cpf'")
                self.voltar_menu()
                return
            
            # Preencher valores vazios e adicionar colunas necessárias
            df.fillna("", inplace=True)  # Usar string vazia em vez de "0"
            for col in ['cod_cliente', 'cod_acordo', 'status', 'observacao']:
                if col not in df.columns:
                    df[col] = ""  # Usar string vazia em vez de "0"
            
            total = len(df)
            batch_size = 25
            linhas_processadas = 0
            tempo_inicio = time.time()
            
            self.atualizar_progresso(0, f"Iniciando processamento de {total} CPFs...")
            
            # Processar em lotes
            for batch_start in range(0, total, batch_size):
                if self.cancelar_flag.is_set():
                    break
                
                if self.parar_flag.is_set():
                    self.atualizar_progresso((linhas_processadas/total)*100, "Processo pausado...")
                    self.parar_flag.wait()
                
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
                progresso = (linhas_processadas / total) * 100
                
                # Calcular tempo estimado
                tempo_passado = time.time() - tempo_inicio
                if linhas_processadas > 0:
                    tempo_estimado_restante = (tempo_passado / linhas_processadas) * (total - linhas_processadas)
                    minutos = int(tempo_estimado_restante // 60)
                    self.atualizar_progresso(progresso, f"Processando: {linhas_processadas}/{total} - {minutos}m restantes")
                else:
                    self.atualizar_progresso(progresso, f"Processando: {linhas_processadas}/{total}")
                
                # Salvar progresso a cada 100 linhas
                if linhas_processadas % 100 == 0:
                    df.to_excel(arquivo_saida, index=False, engine='openpyxl')
            
            # Salvar arquivo final
            df.to_excel(arquivo_saida, index=False, engine='openpyxl')
            
            if not self.cancelar_flag.is_set():
                self.atualizar_progresso(100, "Processamento concluído!")
                messagebox.showinfo("Sucesso", f"Arquivo salvo: {arquivo_saida}")
            
        except Exception as e:
            self.logger.critical(f"Erro crítico em obter dívida: {e}")
            messagebox.showerror("Erro", f"Erro no processamento: {e}")
        
        finally:
            self.voltar_menu()
    
    def abrir_extrair_json(self):
        """Funcionalidade extrair JSON - IMPLEMENTAÇÃO COMPLETA"""
        self.mostrar_progresso("Extrair JSON")
        self.logger.log_user_action("Iniciou Extrair JSON", session_id=self.session_id)
        
        # Habilitar controles
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        # Seleção de arquivo
        arquivo_entrada = filedialog.askopenfilename(
            title="Selecione o arquivo Excel com dados JSON",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo_entrada:
            self.voltar_menu()
            return
        
        # Seleção de local para salvar
        arquivo_saida = filedialog.asksaveasfilename(
            title="Onde salvar o resultado?",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo_saida:
            self.voltar_menu()
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_extrair_json, 
                                args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()
    
    def executar_extrair_json(self, arquivo_entrada, arquivo_saida):
        """Executa extração de dados JSON"""
        try:
            # Ler arquivo
            df = pd.read_excel(arquivo_entrada)
            total_linhas = len(df)
            
            self.atualizar_progresso(0, f"Iniciando extração de {total_linhas} registros JSON...")
            
            # Verificar coluna corpo_requisicao
            if 'corpo_requisicao' not in df.columns:
                messagebox.showerror("Erro", "Arquivo deve conter coluna 'corpo_requisicao'")
                self.voltar_menu()
                return
            
            # Processar dados JSON
            registros = []
            
            for idx, row in df.iterrows():
                if self.cancelar_flag.is_set():
                    break
                
                if self.parar_flag.is_set():
                    self.atualizar_progresso((idx/total_linhas)*100, "Processo pausado...")
                    self.parar_flag.wait()
                
                try:
                    corpo_requisicao = row['corpo_requisicao']
                    
                    # Tentar extrair JSON
                    if pd.notna(corpo_requisicao) and corpo_requisicao.strip():
                        try:
                            dados_json = json.loads(corpo_requisicao)
                            
                            # Extrair campos principais
                            registro = {'linha_original': idx + 1}
                            
                            # Função recursiva para extrair dados
                            def extrair_campos(data, prefix=""):
                                if isinstance(data, dict):
                                    for key, value in data.items():
                                        new_key = f"{prefix}{key}" if prefix else key
                                        if isinstance(value, (dict, list)):
                                            extrair_campos(value, f"{new_key}_")
                                        else:
                                            registro[new_key] = value
                                elif isinstance(data, list):
                                    for i, item in enumerate(data):
                                        extrair_campos(item, f"{prefix}{i}_")
                            
                            extrair_campos(dados_json)
                            registros.append(registro)
                            
                        except json.JSONDecodeError:
                            # JSON inválido
                            registro = {
                                'linha_original': idx + 1,
                                'erro': 'JSON inválido',
                                'corpo_original': str(corpo_requisicao)[:100]
                            }
                            registros.append(registro)
                    else:
                        # Vazio
                        registro = {
                            'linha_original': idx + 1,
                            'erro': 'Campo vazio'
                        }
                        registros.append(registro)
                    
                    # Atualizar progresso
                    progresso = ((idx + 1) / total_linhas) * 100
                    self.atualizar_progresso(progresso, f"Processando JSON {idx + 1}/{total_linhas}")
                    
                except Exception as e:
                    self.logger.error(f"Erro na linha {idx + 1}: {e}")
                    registro = {
                        'linha_original': idx + 1,
                        'erro': f"Erro: {str(e)}"
                    }
                    registros.append(registro)
            
            # Criar DataFrame com resultados
            if registros:
                resultado_df = pd.DataFrame(registros)
                resultado_df.to_excel(arquivo_saida, index=False)
                
                if not self.cancelar_flag.is_set():
                    self.atualizar_progresso(100, "Extração concluída!")
                    messagebox.showinfo("Sucesso", f"Dados extraídos e salvos: {arquivo_saida}")
            else:
                messagebox.showwarning("Aviso", "Nenhum dado foi extraído")
            
        except Exception as e:
            self.logger.critical(f"Erro crítico em extrair JSON: {e}")
            messagebox.showerror("Erro", f"Erro na extração: {e}")
        
        finally:
            self.voltar_menu()
    
    def abrir_conversor(self):
        """Funcionalidade conversor - IMPLEMENTAÇÃO COMPLETA"""
        self.mostrar_progresso("Converter CSV → XLSX")
        self.logger.log_user_action("Iniciou Conversor", session_id=self.session_id)
        
        # Habilitar controles
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        # Seleção de arquivos CSV
        arquivos_csv = filedialog.askopenfilenames(
            title="Selecione os arquivos CSV para converter",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not arquivos_csv:
            self.voltar_menu()
            return
        
        # Seleção de pasta de destino
        pasta_destino = filedialog.askdirectory(
            title="Selecione a pasta onde salvar os arquivos Excel"
        )
        
        if not pasta_destino:
            self.voltar_menu()
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_conversor, 
                                args=(arquivos_csv, pasta_destino))
        thread.daemon = True
        thread.start()
    
    def executar_conversor(self, arquivos_csv, pasta_destino):
        """Executa conversão CSV para XLSX"""
        try:
            total_arquivos = len(arquivos_csv)
            self.atualizar_progresso(0, f"Convertendo {total_arquivos} arquivos...")
            
            arquivos_convertidos = []
            erros = []
            
            for idx, arquivo_csv in enumerate(arquivos_csv):
                if self.cancelar_flag.is_set():
                    break
                
                try:
                    # Detectar delimitador
                    delimitador = ','
                    try:
                        with open(arquivo_csv, 'r', encoding='utf-8') as f:
                            primeira_linha = f.readline()
                            if ';' in primeira_linha:
                                delimitador = ';'
                            elif '\t' in primeira_linha:
                                delimitador = '\t'
                    except:
                        pass
                    
                    # Ler CSV
                    df = pd.read_csv(arquivo_csv, delimiter=delimitador, encoding='utf-8')
                    
                    # Limpar cabeçalhos
                    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", '')
                    
                    # Nome do arquivo de saída
                    nome_base = os.path.splitext(os.path.basename(arquivo_csv))[0]
                    arquivo_xlsx = os.path.join(pasta_destino, f"{nome_base}.xlsx")
                    
                    # Salvar como Excel
                    df.to_excel(arquivo_xlsx, index=False)
                    arquivos_convertidos.append(arquivo_xlsx)
                    
                    # Atualizar progresso
                    progresso = ((idx + 1) / total_arquivos) * 100
                    self.atualizar_progresso(progresso, f"Convertido: {nome_base}.xlsx")
                    
                except Exception as e:
                    self.logger.error(f"Erro ao converter {arquivo_csv}: {e}")
                    erros.append(f"{os.path.basename(arquivo_csv)}: {str(e)}")
            
            if not self.cancelar_flag.is_set():
                self.atualizar_progresso(100, "Conversão concluída!")
                
                mensagem = f"Convertidos {len(arquivos_convertidos)} arquivos para:\n{pasta_destino}"
                if erros:
                    mensagem += f"\n\nErros encontrados:\n" + "\n".join(erros[:5])
                    if len(erros) > 5:
                        mensagem += f"\n... e mais {len(erros) - 5} erros"
                
                messagebox.showinfo("Conversão Concluída", mensagem)
            
        except Exception as e:
            self.logger.critical(f"Erro crítico no conversor: {e}")
            messagebox.showerror("Erro", f"Erro na conversão: {e}")
        
        finally:
            self.voltar_menu()

    def abrir_filtrar_duplicatas(self):
        """Abre interface para resolver duplicatas com regras inteligentes"""
        self.logger.log_user_action("Resolver Duplicatas: Interface aberta")
        
        # Mostrar área de progresso com o nome da operação
        self.mostrar_progresso("Resolver Duplicatas")
        
        # Habilitar controles
        self.btn_parar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        
        # Janela de opções
        opcao = messagebox.askyesnocancel(
            "Resolver Duplicatas 🔄",
            "Escolha uma opção:\n\n"
            "✅ SIM - Usar arquivo de exemplo para testar\n"
            "❌ NÃO - Selecionar meu próprio arquivo\n"
            "🚫 CANCELAR - Voltar ao menu\n\n"
            "📋 Arquivo deve ter colunas: 'cpf', 'data_vencimento', 'numero_prestacao', 'cod_prestacao'\n"
            "📋 Colunas opcionais: 'data_pagamento', 'cod_acordo'\n\n"
            "🎯 Nova lógica inteligente:\n"
            "• Prioriza registros sem data_pagamento\n"
            "• Escolhe cod_acordo=0 quando aplicável\n"
            "• Seleciona menor cod_prestacao como desempate"
        )
        
        if opcao is None:  # Cancelar
            self.voltar_menu()
            return
        elif opcao:  # Usar arquivo de exemplo
            arquivo_entrada = "data/Modelos/arquivo_teste_duplicatas.xlsx"
            if not os.path.exists(arquivo_entrada):
                messagebox.showerror("Erro", f"Arquivo de exemplo não encontrado:\n{arquivo_entrada}")
                self.voltar_menu()
                return
            
            # Sugerir arquivo de saída
            arquivo_saida = filedialog.asksaveasfilename(
                title="Salvar registros corretos resolvidos como",
                defaultextension=".xlsx",
                initialfile="registros_corretos_resolvidos.xlsx",
                filetypes=[("Arquivos Excel", "*.xlsx")]
            )
            if not arquivo_saida:
                self.voltar_menu()
                return
        else:  # Selecionar arquivo próprio
            arquivo_entrada = filedialog.askopenfilename(
                title="Selecionar arquivo Excel para resolver duplicatas",
                filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
            )
            if not arquivo_entrada:
                self.voltar_menu()
                return
            
            # Sugerir nome do arquivo de saída
            base_name = os.path.splitext(os.path.basename(arquivo_entrada))[0]
            pasta_origem = os.path.dirname(arquivo_entrada)
            default_saida = os.path.join(pasta_origem, f"{base_name}_resolvidos.xlsx")
            
            arquivo_saida = filedialog.asksaveasfilename(
                title="Salvar registros corretos resolvidos como",
                defaultextension=".xlsx",
                initialfile=f"{base_name}_resolvidos.xlsx",
                initialdir=pasta_origem,
                filetypes=[("Arquivos Excel", "*.xlsx")]
            )
            if not arquivo_saida:
                self.voltar_menu()
                return
        
        # Executar filtro de duplicatas
        self.executar_filtrar_duplicatas(arquivo_entrada, arquivo_saida)
    
    def executar_filtrar_duplicatas(self, arquivo_entrada, arquivo_saida):
        """Executa a resolução de duplicatas"""
        # Log da operação
        self.logger.log_user_action(f"Resolver Duplicatas: Iniciado", 
                                   entrada=arquivo_entrada, 
                                   saida=arquivo_saida)
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_filtrar_duplicatas_thread, 
                                 args=(arquivo_entrada, arquivo_saida))
        thread.daemon = True
        thread.start()
    
    def executar_filtrar_duplicatas_thread(self, arquivo_entrada, arquivo_saida):
        """Thread para executar resolução de duplicatas"""
        try:
            from src.filtrar_duplicatas import filtrar_duplicatas_cpf_data, salvar_arquivo_com_formatacao
            
            self.atualizar_progresso(10, "📂 Carregando arquivo...")
            
            # Carregar arquivo
            df = pd.read_excel(arquivo_entrada)
            total_inicial = len(df)
            
            self.logger.info(f"Resolver Duplicatas: Arquivo carregado - {total_inicial} registros")
            self.atualizar_progresso(30, f"🔍 Analisando {total_inicial} registros...")
            
            # Verificar se arquivo tem dados
            if total_inicial == 0:
                raise ValueError("❌ Arquivo está vazio")
            
            # Verificar colunas necessárias
            colunas_necessarias = ['cpf', 'data_vencimento', 'numero_prestacao', 'cod_prestacao']
            colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
            
            if colunas_faltantes:
                raise ValueError(f"❌ Colunas não encontradas: {', '.join(colunas_faltantes)}")
            
            # Resolver duplicatas aplicando regras inteligentes
            self.atualizar_progresso(50, "🎯 Aplicando regras inteligentes...")
            df_resolvidos = filtrar_duplicatas_cpf_data(df)
            
            registros_resolvidos = len(df_resolvidos)
            
            if registros_resolvidos == 0:
                raise ValueError("❌ Nenhum duplicado encontrado no arquivo")
            
            self.atualizar_progresso(80, "💾 Salvando registros corretos...")
            
            # Salvar arquivo com formatação (registros corretos escolhidos)
            salvar_arquivo_com_formatacao(df_resolvidos, arquivo_saida)
            
            # Gerar relatório de resolução
            relatorio_file = arquivo_saida.replace('.xlsx', '_relatorio_duplicatas.txt')
            grupos_resolvidos = len(df_resolvidos.groupby(['cpf', 'data_vencimento', 'numero_prestacao']))
            
            with open(relatorio_file, "w", encoding="utf-8") as f:
                f.write(f"=== RELATÓRIO DE RESOLUÇÃO DE DUPLICATAS ===\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Arquivo original: {os.path.basename(arquivo_entrada)}\n")
                f.write(f"Arquivo de resultado: {os.path.basename(arquivo_saida)}\n")
                f.write(f"Total de registros originais: {total_inicial}\n")
                f.write(f"Grupos de duplicatas resolvidos: {grupos_resolvidos}\n")
                f.write(f"Registros corretos escolhidos: {registros_resolvidos}\n")
                f.write(f"Taxa de duplicação: {(grupos_resolvidos/total_inicial*100) if total_inicial > 0 else 0:.1f}%\n")
                f.write("=" * 60 + "\n\n")
                f.write("REGRAS APLICADAS:\n")
                f.write("1. Se tiver data_pagamento: salva linha sem data_pagamento\n")
                f.write("2. Se ambos têm data_pagamento: prioriza cod_acordo=0\n")
                f.write("3. Se ambos têm data_pagamento e cod_acordo: menor cod_prestacao\n")
                f.write("4. Se data_pagamento null: prioriza cod_acordo=0\n")
                f.write("5. Se data_pagamento null e ambos têm cod_acordo: menor cod_prestacao\n")
            
            self.atualizar_progresso(100, "✅ Resolução concluída!")
            
            # Log sucesso
            self.logger.log_user_action(f"Resolver Duplicatas: Concluído com sucesso", 
                                       registros_originais=total_inicial,
                                       grupos_resolvidos=grupos_resolvidos,
                                       registros_corretos_salvos=registros_resolvidos)
            
            # Mostrar resultado
            resultado_msg = f"""✅ Resolução de duplicatas concluída!

📊 Registros originais: {total_inicial:,}
🎯 Grupos de duplicatas: {grupos_resolvidos:,}
✅ Registros corretos escolhidos: {registros_resolvidos:,}
📁 Arquivo salvo: {os.path.basename(arquivo_saida)}
📝 Relatório salvo: {os.path.basename(relatorio_file)}

🎯 Regras aplicadas:
• Prioriza registros sem data_pagamento
• Escolhe cod_acordo=0 quando aplicável  
• Usa menor cod_prestacao como desempate"""
            
            messagebox.showinfo("Resolução Concluída", resultado_msg)
            
        except Exception as e:
            self.logger.error(f"Erro na resolução de duplicatas: {e}")
            self.atualizar_progresso(0, f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro na resolução de duplicatas:\n{str(e)}")
        
        finally:
            # Voltar ao menu
            self.voltar_menu()
    
    def abrir_nolog(self):
        """Abre a interface do NoLogout em uma nova janela"""
        self.logger.log_user_action("Abriu Manter Sessão", session_id=self.session_id)
        
        try:
            # Criar nova janela usando popup centralizado
            nolog_window = self._create_nolog_popup("Manter Sessão", geometry="600x420")

            # Importar e iniciar a interface ManterSessao (português)
            from src.manter_sessao import ManterSessaoGUI

            # Criar instância do ManterSessao na nova janela
            nolog_app = ManterSessaoGUI(nolog_window)
            
            self.logger.info("Manter Sessão iniciado com sucesso")
            
        except Exception as e:
            # Mensagens atualizadas para a nomenclatura em português
            self.logger.error(f"Erro ao abrir Manter Sessão: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir Manter Sessão:\n{str(e)}")
    
    def abrir_separador_dividas(self):
        """Abre a interface do Separador de Dívidas em uma nova janela"""
        self.logger.log_user_action("Abriu Separador de Dívidas", session_id=self.session_id)
        
        try:
            # Criar nova janela usando popup centralizado
            separador_window = self._create_nolog_popup("Separador de Dívidas", geometry="700x520")

            # Importar e iniciar Separador GUI
            from src.separador_dividas import SeparadorDividasGUI

            # Criar instância do Separador na nova janela
            separador_app = SeparadorDividasGUI(separador_window)
            
            self.logger.info("Separador de Dívidas iniciado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao abrir Separador de Dívidas: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir Separador de Dívidas:\n{str(e)}")

    def abrir_consulta_boleto_mensal(self):
        """Abre diálogo para executar a Consulta Boleto Mensal (arquivo ou manual).

        UI melhorada: permite escolher modo 'Arquivo' ou 'Manual', inserir múltiplos períodos
        (uma por linha no formato YYYY-MM) e selecionar arquivo de saída.
        """
        self.logger.log_user_action("Abriu Consulta Boleto Mensal", session_id=self.session_id)

        try:
            dialog = self._create_nolog_popup("📆 Consulta Boleto Mensal", geometry="900x620")
            try:
                dialog.minsize(700, 520)
                dialog.resizable(True, True)
            except Exception:
                pass
            dialog.configure(bg=self.theme_manager.get_color('background'))

            container = self.theme_manager.create_card_frame(dialog, "📆 Consulta Boleto Mensal")
            container.pack(fill='both', expand=True, padx=16, pady=16)

            body = tk.Frame(container, bg=self.theme_manager.get_color('surface'))
            body.pack(fill='both', expand=True, padx=12, pady=12)

            # Modo: arquivo ou manual
            mode_var = tk.StringVar(value='file')
            mode_frame = tk.Frame(body, bg=self.theme_manager.get_color('surface'))
            mode_frame.pack(fill='x', pady=(0, 8))
            tk.Radiobutton(mode_frame, text='📁 Arquivo (vários alunos)', variable=mode_var, value='file', bg=self.theme_manager.get_color('surface')).pack(side='left', padx=6)
            tk.Radiobutton(mode_frame, text='⌨️ Manual (colar/um por linha)', variable=mode_var, value='manual', bg=self.theme_manager.get_color('surface')).pack(side='left', padx=6)

            # File selection area
            file_frame = tk.Frame(body, bg=self.theme_manager.get_color('surface'))
            file_frame.pack(fill='x', pady=(6, 6))
            tk.Label(file_frame, text='Arquivo de entrada (Excel):', bg=self.theme_manager.get_color('surface')).pack(anchor='w')
            entry_file = tk.Entry(file_frame, width=72)
            entry_file.pack(fill='x', pady=(4, 4))

            def pick_input():
                f = filedialog.askopenfilename(title='Selecione o arquivo Excel', filetypes=[('Excel files','*.xlsx'),('All','*.*')])
                if f:
                    entry_file.delete(0, tk.END)
                    entry_file.insert(0, f)

            tk.Button(file_frame, text='Escolher...', command=pick_input).pack(anchor='e')

            # Manual entry area (multiline)
            manual_frame = tk.Frame(body, bg=self.theme_manager.get_color('surface'))
            manual_frame.pack(fill='both', pady=(6, 6))
            tk.Label(manual_frame, text='CPFs (um por linha, sem pontos):', bg=self.theme_manager.get_color('surface')).pack(anchor='w')
            txt_manual = tk.Text(manual_frame, height=4)
            txt_manual.pack(fill='x', pady=(4, 4))

            # Periods area - allow multiple YYYY-MM
            period_frame = tk.Frame(body, bg=self.theme_manager.get_color('surface'))
            period_frame.pack(fill='both', pady=(6, 6))
            tk.Label(period_frame, text='Períodos (uma linha por período - ex: 2025-08):', bg=self.theme_manager.get_color('surface')).pack(anchor='w')
            txt_periods = tk.Text(period_frame, height=3)
            txt_periods.insert('1.0', f"{time.localtime().tm_year}-{time.localtime().tm_mon:02d}")
            txt_periods.pack(fill='x', pady=(4, 4))

            # Output file
            out_frame = tk.Frame(body, bg=self.theme_manager.get_color('surface'))
            out_frame.pack(fill='x', pady=(6, 6))
            tk.Label(out_frame, text='Arquivo de saída (Excel):', bg=self.theme_manager.get_color('surface')).pack(anchor='w')
            entry_out = tk.Entry(out_frame, width=72)
            entry_out.pack(fill='x', pady=(4, 4))

            def pick_output():
                default_name = f"consulta_boleto_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
                f = filedialog.asksaveasfilename(title='Salvar resultado como', defaultextension='.xlsx', initialfile=default_name, filetypes=[('Excel files','*.xlsx')])
                if f:
                    entry_out.delete(0, tk.END)
                    entry_out.insert(0, f)

            tk.Button(out_frame, text='Escolher saída...', command=pick_output).pack(anchor='e')

            # Start / Cancel buttons
            btns = tk.Frame(body, bg=self.theme_manager.get_color('surface'))
            btns.pack(fill='x', pady=(8, 0))

            def start():
                mode = mode_var.get()
                periods_text = txt_periods.get('1.0', 'end').strip()
                period_lines = [l.strip() for l in periods_text.splitlines() if l.strip()]
                arquivo_saida = entry_out.get().strip()
                if not period_lines:
                    messagebox.showerror('Erro', 'Informe ao menos um período (ex: 2025-08)')
                    return
                if not arquivo_saida:
                    messagebox.showerror('Erro', 'Selecione arquivo de saída')
                    return

                if mode == 'file':
                    arquivo_entrada = entry_file.get().strip()
                    if not arquivo_entrada:
                        messagebox.showerror('Erro', 'Selecione arquivo de entrada')
                        return
                    dialog.destroy()
                    thread = threading.Thread(target=self.executar_consulta_boleto_thread, args=(arquivo_entrada, arquivo_saida, period_lines, 'file'))
                    thread.daemon = True
                    thread.start()
                else:
                    manual_text = txt_manual.get('1.0', 'end').strip()
                    if not manual_text:
                        messagebox.showerror('Erro', 'Digite ao menos um CPF manualmente')
                        return
                    # construir rows a partir dos CPFs manualmente (cod_aluno vazio)
                    cpfs = [l.strip() for l in re.split(r'[\n,;]+', manual_text) if l.strip()]
                    rows = [("", c) for c in cpfs]
                    dialog.destroy()
                    thread = threading.Thread(target=self.executar_consulta_boleto_thread, args=(rows, arquivo_saida, period_lines, 'manual'))
                    thread.daemon = True
                    thread.start()

            start_btn = tk.Button(btns, text='▶ Iniciar', command=start)
            self.theme_manager.apply_theme_to_widget(start_btn, 'primary_button')
            start_btn.pack(side='right')

            cancel_btn = tk.Button(btns, text='❌ Fechar', command=dialog.destroy)
            self.theme_manager.apply_theme_to_widget(cancel_btn, 'secondary_button')
            cancel_btn.pack(side='right', padx=(0, 8))

        except Exception as e:
            self.logger.error(f"Erro ao abrir Consulta Boleto Mensal: {e}")
            messagebox.showerror('Erro', f'Erro ao abrir Consulta Boleto Mensal:\n{e}')

    def executar_consulta_boleto_thread(self, arquivo_entrada, arquivo_saida, ano, mes_or_mode):
        """Thread que executa a consulta boleto mensal.

        Args:
            arquivo_entrada: path (str) when mode='file' or list of rows when mode='manual'
            arquivo_saida: output path
            ano: in our new contract holds the periods list
            mes_or_mode: mode string - 'file' or 'manual'
        """
        try:
            from src.consulta_boleto_mensal import run_consulta_boleto, run_consulta_boleto_from_rows

            self.mostrar_progresso('Consulta Boleto Mensal')
            self.atualizar_progresso(5, 'Iniciando consulta...')
            start = time.time()

            mode = mes_or_mode if isinstance(mes_or_mode, str) else 'file'
            # In our call we pass periods via the `ano` parameter
            period_lines = ano

            if mode == 'manual':
                # arquivo_entrada is actually rows list
                rows = arquivo_entrada
                run_consulta_boleto_from_rows(rows, arquivo_saida, period_lines)
            else:
                run_consulta_boleto(arquivo_entrada, arquivo_saida, period_lines)

            elapsed = time.time() - start
            self.atualizar_progresso(100, f'Concluído em {elapsed:.1f}s')
            messagebox.showinfo('Sucesso', f'Consulta concluída! Arquivo salvo:\n{arquivo_saida}')

        except Exception as e:
            self.logger.error(f'Erro em Consulta Boleto Mensal: {e}')
            self.atualizar_progresso(0, f'Erro: {e}')
            messagebox.showerror('Erro', f'Erro durante a execução:\n{e}')
        finally:
            self.voltar_menu()

def main():
    """Função principal"""
    root = tk.Tk()
    app = Python4WorkPro(root)
    
    try:
        root.mainloop()
    except Exception as e:
        if hasattr(app, 'logger'):
            app.logger.critical("Erro crítico na aplicação", exception=e)
        else:
            print(f"Erro crítico: {e}")

if __name__ == "__main__":
    main()
