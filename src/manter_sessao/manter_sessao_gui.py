"""
ManterSessao GUI - Interface gráfica traduzida e compatível com ManterSessaoCore
"""
import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime
import os
from .manter_sessao_core import ManterSessaoCore


class ManterSessaoGUI:
    """Interface gráfica para o ManterSessao"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Manter Sessão - Mantenha sua Sessão Ativa")

        # Inicializa o core com caminho correto do config
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.manter = ManterSessaoCore(config_path)
        self.thread = None
        
        # Cores
        self.bg_color = "#2c3e50"
        self.card_color = "#34495e"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.text_color = "#ecf0f1"
        
        self.root.configure(bg=self.bg_color)
        
        # Cria a interface
        self.create_widgets()
        
        # Ajusta tamanho e centraliza DEPOIS de criar widgets
        self.root.update_idletasks()
        self.center_window()
        
        # Protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centraliza a janela na tela com tamanho adequado"""
        # Define tamanho mínimo e inicial - AUMENTADO
        width = 500
        height = 700
        
        # Calcula posição central
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Aplica geometria e permite redimensionamento
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.minsize(450, 600)  # Tamanho mínimo aumentado
        self.root.resizable(True, True)  # Permite redimensionar
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal com scroll se necessário
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both')
        
        # =================
        # TÍTULO
        # =================
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(pady=(20, 10))
        
        tk.Label(
            title_frame,
            text="🛡️",
            font=("Segoe UI", 40),
            bg=self.bg_color,
            fg=self.text_color
        ).pack()
        
        tk.Label(
            title_frame,
            text="Manter Sessão",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack()
        
        tk.Label(
            title_frame,
            text="Mantenha sua sessão ativa",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#95a5a6"
        ).pack(pady=(3, 0))
        
        # =================
        # STATUS VISUAL
        # =================
        status_frame = tk.Frame(main_frame, bg=self.card_color, height=110)
        status_frame.pack(fill='x', padx=25, pady=15)
        status_frame.pack_propagate(False)
        
        # Indicador circular
        indicator_container = tk.Frame(status_frame, bg=self.card_color)
        indicator_container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.status_canvas = tk.Canvas(
            indicator_container,
            width=60,
            height=60,
            bg=self.card_color,
            highlightthickness=0
        )
        self.status_canvas.pack(side='left', padx=(0, 12))
        
        self.status_circle = self.status_canvas.create_oval(
            8, 8, 52, 52,
            fill=self.danger_color,
            outline=self.danger_color,
            width=3
        )
        
        # Texto de status
        status_text_frame = tk.Frame(indicator_container, bg=self.card_color)
        status_text_frame.pack(side='left')
        
        self.status_label = tk.Label(
            status_text_frame,
            text="PARADO",
            font=("Segoe UI", 18, "bold"),
            bg=self.card_color,
            fg=self.danger_color
        )
        self.status_label.pack(anchor='w')
        
        self.status_desc = tk.Label(
            status_text_frame,
            text="Clique no botão INICIAR abaixo",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        )
        self.status_desc.pack(anchor='w')
        
        # =================
        # ESTATÍSTICAS
        # =================
        stats_frame = tk.Frame(main_frame, bg=self.card_color)
        stats_frame.pack(fill='x', padx=25, pady=(0, 15))
        
        # Contador de ações
        counter_frame = tk.Frame(stats_frame, bg=self.card_color)
        counter_frame.pack(pady=12)
        
        self.actions_label = tk.Label(
            counter_frame,
            text="0",
            font=("Segoe UI", 36, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        self.actions_label.pack()
        
        tk.Label(
            counter_frame,
            text="AÇÕES REALIZADAS",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        ).pack()
        
        # Linha separadora
        separator = tk.Frame(stats_frame, bg="#7f8c8d", height=1)
        separator.pack(fill='x', padx=20, pady=8)
        
        # Informações de configuração
        info_frame = tk.Frame(stats_frame, bg=self.card_color)
        info_frame.pack(pady=(4, 12))
        
        config = self.manter.config
        
        tk.Label(
            info_frame,
            text=f"Intervalo: {config['interval_seconds']} segundos",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        ).pack()
        
        self.time_label = tk.Label(
            info_frame,
            text="Última ação: Nenhuma",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        )
        self.time_label.pack(pady=(2, 0))
        
        # Toggle de som
        sound_frame = tk.Frame(stats_frame, bg=self.card_color)
        sound_frame.pack(pady=(5, 8))
        
        self.sound_var = tk.BooleanVar(value=config.get('sound_enabled', True))
        sound_check = tk.Checkbutton(
            sound_frame,
            text="🔊 Sons de notificação",
            variable=self.sound_var,
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6",
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground="#ecf0f1",
            command=self.toggle_sound
        )
        sound_check.pack()
        
        # =================
        # BOTÃO ÚNICO - LIGA/DESLIGA
        # =================
        button_container = tk.Frame(main_frame, bg=self.bg_color)
        button_container.pack(fill='both', expand=True, padx=30, pady=(10, 30))
        
        # Botão ÚNICO que alterna entre INICIAR e PARAR
        self.toggle_button = tk.Button(
            button_container,
            text="▶  INICIAR PROTEÇÃO",
            font=("Segoe UI", 16, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief='raised',
            cursor='hand2',
            command=self.toggle_protection,
            bd=4,
            pady=25
        )
        self.toggle_button.pack(fill='both', expand=True, ipady=15)
        
        # Label de instrução
        instruction_label = tk.Label(
            button_container,
            text="Clique no botão para Iniciar ou Parar",
            font=("Segoe UI", 10, "italic"),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        instruction_label.pack(pady=(10, 0))
        
        # Espaço extra no final
        spacer = tk.Frame(main_frame, bg=self.bg_color, height=10)
        spacer.pack()
    
    def update_status_callback(self, success: bool, total_actions: int):
        """Callback para atualizar a interface"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Atualiza na thread principal
        self.root.after(0, lambda: self.actions_label.config(text=str(total_actions)))
        self.root.after(0, lambda: self.time_label.config(text=f"Última ação: {timestamp}"))
    
    def toggle_sound(self):
        """Ativa/desativa sons de notificação"""
        self.manter.config['sound_enabled'] = self.sound_var.get()
        # Toca um som de teste
        if self.sound_var.get():
            self.manter.play_sound('start')
    
    def toggle_protection(self):
        """Alterna entre iniciar e parar a proteção"""
        if self.manter.running:
            # Se está rodando, para
            self.stop_protection()
        else:
            # Se está parado, inicia
            self.start_protection()
    
    def start_protection(self):
        """Inicia a proteção"""
        if self.thread and self.thread.is_alive():
            return
        
        # Atualiza botão para modo PARAR
        self.toggle_button.config(
            text="■  PARAR PROTEÇÃO",
            bg=self.danger_color,
            activebackground="#c0392b"
        )
        
        # Atualiza status visual
        self.status_canvas.itemconfig(self.status_circle, fill=self.success_color, outline=self.success_color)
        self.status_label.config(text="ATIVO", fg=self.success_color)
        self.status_desc.config(text="Sua sessão está protegida")
        
        # Inicia thread
        self.thread = threading.Thread(
            target=self.manter.start,
            args=(self.update_status_callback,),
            daemon=True
        )
        self.thread.start()
    
    def stop_protection(self):
        """Para a proteção"""
        if self.manter.running:
            self.manter.stop()
        
        # Atualiza botão para modo INICIAR
        self.toggle_button.config(
            text="▶  INICIAR PROTEÇÃO",
            bg=self.success_color,
            activebackground="#229954"
        )
        
        # Atualiza status visual
        self.status_canvas.itemconfig(self.status_circle, fill=self.danger_color, outline=self.danger_color)
        self.status_label.config(text="PARADO", fg=self.danger_color)
        self.status_desc.config(text="Clique no botão INICIAR")
    
    def on_closing(self):
        """Trata o fechamento da janela"""
        if self.manter.running:
            if messagebox.askokcancel("Sair", "A proteção está ativa. Deseja realmente sair?"):
                self.stop_protection()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Função principal para testes rápidos"""
    root = tk.Tk()
    app = ManterSessaoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
"""
ManterSessao GUI - Interface gráfica simples e funcional (tradução para português)
"""
import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime
import os
from .manter_sessao_core import ManterSessaoCore


class ManterSessaoGUI:
    """Interface gráfica para o ManterSessao"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Manter Sessão - Mantenha sua Sessão Ativa")

        # Inicializa o core com caminho correto do config
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.nolog = ManterSessaoCore(config_path)
        self.thread = None
        
        # Cores
        self.bg_color = "#2c3e50"
        self.card_color = "#34495e"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.text_color = "#ecf0f1"
        
        self.root.configure(bg=self.bg_color)
        
        # Cria a interface
        self.create_widgets()
        
        # Ajusta tamanho e centraliza DEPOIS de criar widgets
        self.root.update_idletasks()
        self.center_window()
        
        # Protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centraliza a janela na tela com tamanho adequado"""
        # Define tamanho mínimo e inicial - AUMENTADO
        width = 500
        height = 700
        
        # Calcula posição central
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Aplica geometria e permite redimensionamento
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.minsize(450, 600)  # Tamanho mínimo aumentado
        self.root.resizable(True, True)  # Permite redimensionar
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal com scroll se necessário
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both')
        
        # =================
        # TÍTULO
        # =================
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(pady=(20, 10))
        
        tk.Label(
            title_frame,
            text="🛡️",
            font=("Segoe UI", 40),
            bg=self.bg_color,
            fg=self.text_color
        ).pack()
        
        tk.Label(
            title_frame,
            text="Manter Sessão",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack()
        
        tk.Label(
            title_frame,
            text="Mantenha sua sessão ativa",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#95a5a6"
        ).pack(pady=(3, 0))
        
        # Restante da interface (mantida igual ao original, apenas textos atualizados)
        status_frame = tk.Frame(main_frame, bg=self.card_color, height=110)
        status_frame.pack(fill='x', padx=25, pady=15)
        status_frame.pack_propagate(False)
        
        indicator_container = tk.Frame(status_frame, bg=self.card_color)
        indicator_container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.status_canvas = tk.Canvas(
            indicator_container,
            width=60,
            height=60,
            bg=self.card_color,
            highlightthickness=0
        )
        self.status_canvas.pack(side='left', padx=(0, 12))
        
        self.status_circle = self.status_canvas.create_oval(
            8, 8, 52, 52,
            fill=self.danger_color,
            outline=self.danger_color,
            width=3
        )
        
        status_text_frame = tk.Frame(indicator_container, bg=self.card_color)
        status_text_frame.pack(side='left')
        
        self.status_label = tk.Label(
            status_text_frame,
            text="PARADO",
            font=("Segoe UI", 18, "bold"),
            bg=self.card_color,
            fg=self.danger_color
        )
        self.status_label.pack(anchor='w')
        
        self.status_desc = tk.Label(
            status_text_frame,
            text="Clique no botão INICIAR abaixo",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        )
        self.status_desc.pack(anchor='w')
        
        stats_frame = tk.Frame(main_frame, bg=self.card_color)
        stats_frame.pack(fill='x', padx=25, pady=(0, 15))
        
        counter_frame = tk.Frame(stats_frame, bg=self.card_color)
        counter_frame.pack(pady=12)
        
        self.actions_label = tk.Label(
            counter_frame,
            text="0",
            font=("Segoe UI", 36, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        self.actions_label.pack()
        
        tk.Label(
            counter_frame,
            text="AÇÕES REALIZADAS",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        ).pack()
        
        separator = tk.Frame(stats_frame, bg="#7f8c8d", height=1)
        separator.pack(fill='x', padx=20, pady=8)
        
        info_frame = tk.Frame(stats_frame, bg=self.card_color)
        info_frame.pack(pady=(4, 12))
        
        config = self.nolog.config
        
        tk.Label(
            info_frame,
            text=f"Intervalo: {config['interval_seconds']} segundos",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        ).pack()
        
        self.time_label = tk.Label(
            info_frame,
            text="Última ação: Nenhuma",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6"
        )
        self.time_label.pack(pady=(2, 0))
        
        sound_frame = tk.Frame(stats_frame, bg=self.card_color)
        sound_frame.pack(pady=(5, 8))
        
        self.sound_var = tk.BooleanVar(value=config.get('sound_enabled', True))
        sound_check = tk.Checkbutton(
            sound_frame,
            text="🔊 Sons de notificação",
            variable=self.sound_var,
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#95a5a6",
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground="#ecf0f1",
            command=self.toggle_sound
        )
        sound_check.pack()
        
        button_container = tk.Frame(main_frame, bg=self.bg_color)
        button_container.pack(fill='both', expand=True, padx=30, pady=(10, 30))
        
        self.toggle_button = tk.Button(
            button_container,
            text="▶  INICIAR PROTEÇÃO",
            font=("Segoe UI", 16, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief='raised',
            cursor='hand2',
            command=self.toggle_protection,
            bd=4,
            pady=25
        )
        self.toggle_button.pack(fill='both', expand=True, ipady=15)
        
        instruction_label = tk.Label(
            button_container,
            text="Clique no botão para Iniciar ou Parar",
            font=("Segoe UI", 10, "italic"),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        instruction_label.pack(pady=(10, 0))
        
        spacer = tk.Frame(main_frame, bg=self.bg_color, height=10)
        spacer.pack()
    
    def update_status_callback(self, success: bool, total_actions: int):
        """Callback para atualizar a interface"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Atualiza na thread principal
        self.root.after(0, lambda: self.actions_label.config(text=str(total_actions)))
        self.root.after(0, lambda: self.time_label.config(text=f"Última ação: {timestamp}"))
    
    def toggle_sound(self):
        """Ativa/desativa sons de notificação"""
        self.nolog.config['sound_enabled'] = self.sound_var.get()
        # Toca um som de teste
        if self.sound_var.get():
            self.nolog.play_sound('start')
    
    def toggle_protection(self):
        """Alterna entre iniciar e parar a proteção"""
        if self.nolog.running:
            # Se está rodando, para
            self.stop_protection()
        else:
            # Se está parado, inicia
            self.start_protection()
    
    def start_protection(self):
        """Inicia a proteção"""
        if self.thread and self.thread.is_alive():
            return
        
        # Atualiza botão para modo PARAR
        self.toggle_button.config(
            text="■  PARAR PROTEÇÃO",
            bg=self.danger_color,
            activebackground="#c0392b"
        )
        
        # Atualiza status visual
        self.status_canvas.itemconfig(self.status_circle, fill=self.success_color, outline=self.success_color)
        self.status_label.config(text="ATIVO", fg=self.success_color)
        self.status_desc.config(text="Sua sessão está protegida")
        
        # Inicia thread
        self.thread = threading.Thread(
            target=self.nolog.start,
            args=(self.update_status_callback,),
            daemon=True
        )
        self.thread.start()
    
    def stop_protection(self):
        """Para a proteção"""
        if self.nolog.running:
            self.nolog.stop()
        
        # Atualiza botão para modo INICIAR
        self.toggle_button.config(
            text="▶  INICIAR PROTEÇÃO",
            bg=self.success_color,
            activebackground="#229954"
        )
        
        # Atualiza status visual
        self.status_canvas.itemconfig(self.status_circle, fill=self.danger_color, outline=self.danger_color)
        self.status_label.config(text="PARADO", fg=self.danger_color)
        self.status_desc.config(text="Clique no botão INICIAR")
    
    def on_closing(self):
        """Trata o fechamento da janela"""
        if self.nolog.running:
            if messagebox.askokcancel("Sair", "A proteção está ativa. Deseja realmente sair?"):
                self.stop_protection()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Função principal"""
    root = tk.Tk()
    app = ManterSessaoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
