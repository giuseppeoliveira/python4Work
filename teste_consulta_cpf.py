#!/usr/bin/env python3
"""
Teste para validar a funcionalidade melhorada de consulta de CPF
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from obter_divida_cpf import consultar_easycollector, processar_linha_cpf, LOGIN_FIXO, SENHA_FIXO
    print("✅ Módulos importados com sucesso!")
except ImportError as e:
    print(f"❌ Erro na importação: {e}")
    sys.exit(1)

def testar_cpf_individual(cpf_teste):
    """Testa um CPF individual"""
    print(f"\n🔍 TESTANDO CPF: {cpf_teste}")
    print("=" * 50)
    
    try:
        id_cliente, id_acordo, datas = consultar_easycollector(cpf_teste, LOGIN_FIXO, SENHA_FIXO)
        
        print(f"📊 RESULTADOS:")
        print(f"   • IdCliente: {id_cliente}")
        print(f"   • IdAcordo: {id_acordo}")
        print(f"   • Datas Vencimento: {len(datas)} encontradas")
        
        if datas:
            print(f"   • Primeiras 3 datas: {datas[:3]}")
        
        # Simular processamento completo
        row_data = (0, {
            'cpf': cpf_teste,
            'cod_cliente': '0',
            'cod_acordo': '0'
        })
        
        i, status, observacao, new_cod_cliente, new_cod_acordo = processar_linha_cpf(row_data)
        
        print(f"\n📋 PROCESSAMENTO COMPLETO:")
        print(f"   • Status: {status}")
        print(f"   • Observação: {observacao}")
        print(f"   • Novo cod_cliente: {new_cod_cliente}")
        print(f"   • Novo cod_acordo: {new_cod_acordo}")
        
        return {
            'cpf': cpf_teste,
            'id_cliente': id_cliente,
            'id_acordo': id_acordo,
            'datas_count': len(datas),
            'status': status,
            'observacao': observacao,
            'sucesso': True
        }
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return {
            'cpf': cpf_teste,
            'erro': str(e),
            'sucesso': False
        }

def main():
    """Função principal de teste"""
    print("🚀 INICIANDO TESTE DA FUNCIONALIDADE MELHORADA DE CONSULTA CPF")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Verificar credenciais
    if not LOGIN_FIXO or not SENHA_FIXO:
        print("❌ ERRO: Credenciais não configuradas no arquivo .env")
        return
    
    print(f"✅ Credenciais carregadas: Login = {LOGIN_FIXO[:3]}***")
    
    # Lista de CPFs para teste (você pode modificar)
    cpfs_teste = [
        "12345678901",  # CPF exemplo 1
        "98765432100",  # CPF exemplo 2
        "11111111111",  # CPF exemplo 3
    ]
    
    print(f"\n📋 Testando {len(cpfs_teste)} CPFs...")
    
    resultados = []
    
    for i, cpf in enumerate(cpfs_teste, 1):
        print(f"\n{'='*60}")
        print(f"TESTE {i}/{len(cpfs_teste)}")
        resultado = testar_cpf_individual(cpf)
        resultados.append(resultado)
    
    # Resumo dos resultados
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    
    sucessos = sum(1 for r in resultados if r.get('sucesso', False))
    
    print(f"✅ Sucessos: {sucessos}/{len(resultados)}")
    print(f"❌ Erros: {len(resultados) - sucessos}/{len(resultados)}")
    
    for resultado in resultados:
        if resultado.get('sucesso'):
            print(f"   • CPF {resultado['cpf']}: IdCliente={resultado['id_cliente']}, IdAcordo={resultado['id_acordo']}, Status={resultado['status']}")
        else:
            print(f"   • CPF {resultado['cpf']}: ERRO = {resultado.get('erro', 'Desconhecido')}")
    
    print(f"\n🏁 TESTE CONCLUÍDO!")
    
    # Salvar resultados em arquivo para análise
    try:
        df_resultados = pd.DataFrame(resultados)
        arquivo_resultado = f"teste_cpf_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_resultados.to_excel(arquivo_resultado, index=False)
        print(f"📄 Resultados salvos em: {arquivo_resultado}")
    except Exception as e:
        print(f"⚠️ Não foi possível salvar resultados: {e}")

if __name__ == "__main__":
    main()
