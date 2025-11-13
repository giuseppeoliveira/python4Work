"""
NoLogout GUI - Interface gráfica simples e funcional (rename de NoLog)
"""
import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime
import os
from .nologout_core import NoLogoutCore


class NoLogoutGUI:
    """Interface gráfica para o NoLogout"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NoLogout - Mantenha sua Sessão Ativa")

        # Inicializa o core com caminho correto do config
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.nolog = NoLogoutCore(config_path)
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
            text="NoLogout",
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

        # ... (restante do GUI copiado) ...

def main():
    """Função principal"""
    root = tk.Tk()
    app = NoLogoutGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
