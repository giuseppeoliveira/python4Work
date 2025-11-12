"""
NoLog CLI - Interface de linha de comando
"""
import sys
from datetime import datetime
from nolog_core import NoLogCore


def print_status(success: bool, total_actions: int):
    """Imprime status da última ação"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status = "✓" if success else "✗"
    print(f"[{timestamp}] {status} Ação #{total_actions} executada", end='\r')


def main():
    """Função principal do CLI"""
    print("=" * 60)
    print("🚀 NoLog - Prevenção de Logout Automático")
    print("=" * 60)
    print()
    
    try:
        nolog = NoLogCore()
        nolog.start(callback=print_status)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
