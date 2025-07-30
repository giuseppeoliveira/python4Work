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

# Importar sistemas profissionais
from config_manager import ConfigManager
from professional_logger import ProfessionalLogger
from data_validator import DataValidator
from theme_manager import ThemeManager

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
        self.logger = ProfessionalLogger("Python4WorkPro", self.config)
        self.validator = DataValidator(self.logger)
        self.theme_manager = ThemeManager()
        
        # Iniciar sessão de logging
        self.session_logger = self.logger.create_session_log(self.session_id)
        
        # Configurar tema
        self.theme_manager.set_theme(self.config.get('app.theme', 'modern'))
        
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
        
        # Header com informações da aplicação
        self.criar_header()
        
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
        """Cria header profissional da aplicação"""
        header_frame = self.theme_manager.create_card_frame(self.scrollable_frame)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Container interno
        header_content = tk.Frame(header_frame, bg=self.theme_manager.get_color('surface'))
        header_content.pack(fill='x', padx=20, pady=20)
        
        # Título principal
        title_label = tk.Label(header_content, 
                              text=f"🏢 {self.config.get('app.name', 'Python4Work Professional')}", 
                              font=("Arial", 20, "bold"))
        self.theme_manager.apply_theme_to_widget(title_label, 'title')
        title_label.pack(anchor='w')
        
        # Subtítulo
        subtitle_label = tk.Label(header_content, 
                                 text="Central Profissional de Automação de Processos",
                                 font=("Arial", 12))
        self.theme_manager.apply_theme_to_widget(subtitle_label, 'description')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Informações da sessão
        info_frame = tk.Frame(header_content, bg=self.theme_manager.get_color('surface'))
        info_frame.pack(fill='x', pady=(15, 0))
        
        session_info = f"📋 Sessão: {self.session_id} | 🎨 Tema: {self.theme_manager.get_theme()['name']} | ⚡ Versão: {self.config.get('app.version', '2.0.0')}"
        info_label = tk.Label(info_frame, text=session_info, font=("Arial", 9))
        self.theme_manager.apply_theme_to_widget(info_label, 'description')
        info_label.pack(anchor='w')
        
        # Botões de configuração
        config_frame = tk.Frame(header_content, bg=self.theme_manager.get_color('surface'))
        config_frame.pack(fill='x', pady=(10, 0))
        
        # Botão configurações
        btn_config = tk.Button(config_frame, text="⚙️ Configurações", 
                              command=self.abrir_configuracoes,
                              font=("Arial", 9, "bold"), padx=15, pady=5)
        self.theme_manager.apply_theme_to_widget(btn_config, 'secondary_button')
        btn_config.pack(side='left', padx=(0, 10))
        
        # Botão relatórios
        btn_reports = tk.Button(config_frame, text="📊 Relatórios", 
                               command=self.abrir_relatorios,
                               font=("Arial", 9, "bold"), padx=15, pady=5)
        self.theme_manager.apply_theme_to_widget(btn_reports, 'secondary_button')
        btn_reports.pack(side='left', padx=(0, 10))
        
        # Status de conectividade
        self.status_connectivity = tk.Label(config_frame, text="🔗 Verificando conectividade...", 
                                           font=("Arial", 9))
        self.theme_manager.apply_theme_to_widget(self.status_connectivity, 'description')
        self.status_connectivity.pack(side='right')
        
        # Verificar conectividade em background
        threading.Thread(target=self.verificar_conectividade, daemon=True).start()
    
    def criar_cards_funcionalidades(self):
        """Cria cards das funcionalidades com design profissional e responsivo"""
        # Container dos cards
        cards_container = tk.Frame(self.scrollable_frame, bg=self.theme_manager.get_color('background'))
        cards_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Configurar grid responsivo - 2 colunas em telas normais, 1 em telas pequenas
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)
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
        
        # Criar janela de configurações
        config_window = tk.Toplevel(self.root)
        config_window.title("⚙️ Configurações")
        config_window.geometry("500x400")
        config_window.transient(self.root)
        config_window.grab_set()
        
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
        
        # Configurações de tema
        theme_frame = tk.LabelFrame(main_frame, text="🎨 Tema Visual", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        self.theme_manager.apply_theme_to_widget(theme_frame, 'surface')
        theme_frame.pack(fill='x', pady=(0, 15))
        
        current_theme = self.config.get('app.theme', 'modern')
        theme_var = tk.StringVar(value=current_theme)
        
        themes = [("🌟 Moderno", "modern"), ("🌙 Escuro", "dark"), 
                 ("🏢 Corporativo", "corporate"), ("🌿 Natureza", "nature")]
        
        for text, value in themes:
            rb = tk.Radiobutton(theme_frame, text=text, variable=theme_var, value=value,
                               command=lambda v=value: self.aplicar_tema(v))
            self.theme_manager.apply_theme_to_widget(rb, 'surface')
            rb.pack(anchor='w')
        
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
            self.config.set('app.theme', theme_var.get())
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
        
        # Criar janela de relatórios
        report_window = tk.Toplevel(self.root)
        report_window.title("📊 Relatórios e Logs")
        report_window.geometry("700x500")
        report_window.transient(self.root)
        report_window.grab_set()
        
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
            "Consultar Acordo",
            "Escolha uma opção:\n\n"
            "✅ SIM - Baixar modelo Excel primeiro\n"
            "❌ NÃO - Usar arquivo existente\n"
            "🚫 CANCELAR - Voltar ao menu"
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
    
    def executar_consultar_acordo(self, arquivo_entrada, arquivo_saida):
        """Executa consulta de acordo"""
        try:
            # Importar função do script original
            from consultar_acordo import consultar_status_acordo
            
            # Ler arquivo
            df = pd.read_excel(arquivo_entrada)
            total_linhas = len(df)
            
            self.atualizar_progresso(0, f"Iniciando processamento de {total_linhas} registros...")
            
            # Verificar colunas necessárias
            if not all(col in df.columns for col in ['cod_cliente', 'cod_acordo']):
                messagebox.showerror("Erro", "Arquivo deve conter colunas 'cod_cliente' e 'cod_acordo'")
                self.voltar_menu()
                return
            
            # Adicionar coluna de status se não existir
            if 'status_acordo' not in df.columns:
                df['status_acordo'] = ''
            
            # Processar cada linha
            for idx, row in df.iterrows():
                if self.cancelar_flag.is_set():
                    break
                
                if self.parar_flag.is_set():
                    self.atualizar_progresso((idx/total_linhas)*100, "Processo pausado...")
                    self.parar_flag.wait()
                
                try:
                    cod_cliente = str(row['cod_cliente']).strip()
                    cod_acordo = str(row['cod_acordo']).strip()
                    
                    # Consultar acordo (função espera row e index)
                    status = consultar_status_acordo(row, idx)
                    df.at[idx, 'status_acordo'] = status
                    
                    # Atualizar progresso
                    progresso = ((idx + 1) / total_linhas) * 100
                    self.atualizar_progresso(progresso, f"Processando linha {idx + 1}/{total_linhas}")
                    
                    # Salvar periodicamente
                    if (idx + 1) % 5 == 0:
                        df.to_excel(arquivo_saida, index=False)
                    
                except Exception as e:
                    self.logger.error(f"Erro na linha {idx + 1}: {e}")
                    df.at[idx, 'status_acordo'] = f"ERRO: {str(e)}"
            
            # Salvar resultado final
            df.to_excel(arquivo_saida, index=False)
            
            if not self.cancelar_flag.is_set():
                self.atualizar_progresso(100, "Processamento concluído!")
                messagebox.showinfo("Sucesso", f"Arquivo salvo: {arquivo_saida}")
            
        except Exception as e:
            self.logger.critical(f"Erro crítico em consultar acordo: {e}")
            messagebox.showerror("Erro", f"Erro no processamento: {e}")
        
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
        """Executa obtenção de dívida por CPF"""
        try:
            # Importar função do script original
            from obter_divida_cpf import consultar_easycollector
            
            # Ler arquivo
            df = pd.read_excel(arquivo_entrada)
            total_linhas = len(df)
            
            self.atualizar_progresso(0, f"Iniciando processamento de {total_linhas} CPFs...")
            
            # Verificar coluna CPF
            if 'cpf' not in df.columns:
                messagebox.showerror("Erro", "Arquivo deve conter coluna 'cpf'")
                self.voltar_menu()
                return
            
            # Adicionar colunas de resultado se não existirem
            for col in ['cod_cliente', 'cod_acordo', 'status', 'observacao']:
                if col not in df.columns:
                    df[col] = ''
            
            # Processar cada linha
            for idx, row in df.iterrows():
                if self.cancelar_flag.is_set():
                    break
                
                if self.parar_flag.is_set():
                    self.atualizar_progresso((idx/total_linhas)*100, "Processo pausado...")
                    self.parar_flag.wait()
                
                try:
                    cpf = str(row['cpf']).strip()
                    
                    # Validar CPF
                    if not self.validator.validate_cpf(cpf):
                        df.at[idx, 'status'] = 'CPF Inválido'
                        df.at[idx, 'observacao'] = 'CPF não passou na validação'
                        continue
                    
                    # Consultar dívida
                    resultado = consultar_easycollector(cpf, LOGIN, SENHA)
                    
                    if resultado and len(resultado) >= 4:
                        df.at[idx, 'cod_cliente'] = resultado[0]
                        df.at[idx, 'cod_acordo'] = resultado[1]
                        df.at[idx, 'status'] = resultado[2]
                        df.at[idx, 'observacao'] = resultado[3]
                    else:
                        df.at[idx, 'status'] = 'Não encontrado'
                        df.at[idx, 'observacao'] = 'CPF não retornou dados'
                    
                    # Atualizar progresso
                    progresso = ((idx + 1) / total_linhas) * 100
                    self.atualizar_progresso(progresso, f"Processando CPF {idx + 1}/{total_linhas}")
                    
                    # Salvar periodicamente
                    if (idx + 1) % 5 == 0:
                        df.to_excel(arquivo_saida, index=False)
                    
                except Exception as e:
                    self.logger.error(f"Erro no CPF linha {idx + 1}: {e}")
                    df.at[idx, 'status'] = 'ERRO'
                    df.at[idx, 'observacao'] = f"Erro: {str(e)}"
            
            # Salvar resultado final
            df.to_excel(arquivo_saida, index=False)
            
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
