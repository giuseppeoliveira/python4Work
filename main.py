#!/usr/bin/env python3
"""
Script de inicialização do Python4Work Professional
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz do projeto ao sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    try:
        import tkinter as tk
        from interfaces.interface_profissional import Python4WorkPro
        
        # Criar e executar a interface
        root = tk.Tk()
        app = Python4WorkPro(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Verifique se todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        sys.exit(1)
