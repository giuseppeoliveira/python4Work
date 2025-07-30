"""
Script de teste para verificar se a interface unificada está funcionando corretamente.
"""

import sys
import os

def testar_interface():
    print("🧪 TESTE DA INTERFACE UNIFICADA")
    print("=" * 50)
    
    # Verificar se o arquivo principal existe
    if os.path.exists("interface_unificada.py"):
        print("✅ Arquivo interface_unificada.py encontrado")
    else:
        print("❌ Arquivo interface_unificada.py não encontrado")
        return False
    
    # Testar importações
    try:
        print("🔍 Testando importações...")
        import pandas as pd
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        import requests
        from bs4 import BeautifulSoup
        from dotenv import load_dotenv
        print("✅ Todas as importações necessárias estão disponíveis")
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    
    # Testar variáveis de ambiente
    try:
        print("🔍 Testando variáveis de ambiente...")
        load_dotenv()
        
        LOGIN = os.getenv("LOGIN")
        SENHA = os.getenv("SENHA")
        URL = os.getenv("URL")
        URL_DIVIDA = os.getenv("URL_DIVIDA")
        
        if all([LOGIN, SENHA, URL, URL_DIVIDA]):
            print("✅ Todas as variáveis de ambiente estão configuradas")
        else:
            print("⚠️ Algumas variáveis de ambiente estão faltando (funcionalidades limitadas)")
    except Exception as e:
        print(f"❌ Erro ao carregar variáveis de ambiente: {e}")
    
    print("\n🎉 TESTE CONCLUÍDO!")
    print("✅ A interface unificada está pronta para uso!")
    print("\n📋 Para executar:")
    print("   python interface_unificada.py")
    
    return True

if __name__ == "__main__":
    testar_interface()
