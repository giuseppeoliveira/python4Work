#!/usr/bin/env python3
"""
Teste específico para CPFs que você sabe que possuem cod_acordo e cod_cliente
Execute este script para validar se o problema foi resolvido
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def executar_teste_cpf_conhecido():
    """
    Execute este teste com um CPF que você sabe manualmente que possui códigos
    """
    
    print("🎯 TESTE ESPECÍFICO - CPF COM CÓDIGOS CONHECIDOS")
    print("=" * 60)
    print("INSTRUÇÕES:")
    print("1. Substitua o CPF_TESTE abaixo por um CPF que você consultou manualmente")
    print("2. Execute o script")
    print("3. Compare os resultados com o que você viu manualmente")
    print("=" * 60)
    
    # ⚠️ SUBSTITUA ESTE CPF POR UM QUE VOCÊ SABE QUE TEM CÓDIGOS
    CPF_TESTE = "12345678901"  # ← MUDE AQUI
    
    print(f"📋 CPF sendo testado: {CPF_TESTE}")
    print("⚠️  IMPORTANTE: Certifique-se de que este CPF realmente possui códigos!")
    
    try:
        from obter_divida_cpf import consultar_easycollector, LOGIN_FIXO, SENHA_FIXO
        
        print(f"\n🔍 Consultando CPF {CPF_TESTE}...")
        
        id_cliente, id_acordo, datas = consultar_easycollector(CPF_TESTE, LOGIN_FIXO, SENHA_FIXO)
        
        print(f"\n📊 RESULTADOS DA NOVA IMPLEMENTAÇÃO:")
        print(f"   • IdCliente encontrado: {id_cliente}")
        print(f"   • IdAcordo encontrado: {id_acordo}")
        print(f"   • Quantidade de datas: {len(datas)}")
        
        if id_cliente != 0 or id_acordo != 0:
            print("✅ SUCESSO! A nova implementação encontrou os códigos!")
            print("🎉 O problema parece ter sido resolvido!")
        else:
            print("⚠️  ATENÇÃO: Ainda não encontrou os códigos...")
            print("💡 Possíveis causas:")
            print("   1. O XML retornado não contém os códigos esperados")
            print("   2. A estrutura do XML é diferente do esperado")
            print("   3. Os códigos estão em outros campos")
            
        print(f"\n📝 Para diagnosticar melhor, verifique os logs detalhados acima.")
        print(f"📝 Os primeiros {5} CPFs processados terão debug completo.")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("💡 Verifique:")
        print("   1. Arquivo .env com LOGIN e SENHA")
        print("   2. Conexão com internet")
        print("   3. Se a API está funcionando")

def criar_arquivo_teste_com_cpfs_conhecidos():
    """
    Cria um arquivo Excel de teste com CPFs que você pode testar
    """
    print("\n📄 CRIANDO ARQUIVO DE TESTE...")
    
    # Dados de exemplo - SUBSTITUA pelos seus CPFs conhecidos
    dados_teste = [
        {"cpf": "12345678901", "nome": "Teste 1", "cod_cliente": "0", "cod_acordo": "0", "status": "", "observacao": ""},
        {"cpf": "98765432100", "nome": "Teste 2", "cod_cliente": "0", "cod_acordo": "0", "status": "", "observacao": ""},
        {"cpf": "11111111111", "nome": "Teste 3", "cod_cliente": "0", "cod_acordo": "0", "status": "", "observacao": ""},
    ]
    
    df = pd.DataFrame(dados_teste)
    arquivo_teste = f"teste_cpfs_conhecidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        df.to_excel(arquivo_teste, index=False)
        print(f"✅ Arquivo criado: {arquivo_teste}")
        print("📋 Agora você pode:")
        print("   1. Substituir os CPFs pelos que você sabe que têm códigos")
        print("   2. Usar este arquivo na interface principal")
        print("   3. Verificar se os códigos são encontrados")
        return arquivo_teste
    except Exception as e:
        print(f"❌ Erro ao criar arquivo: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE ESPECÍFICO")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Executar teste com CPF específico
    executar_teste_cpf_conhecido()
    
    # Criar arquivo de teste
    arquivo_criado = criar_arquivo_teste_com_cpfs_conhecidos()
    
    print(f"\n🏁 TESTE CONCLUÍDO!")
    print(f"📝 Próximos passos:")
    print(f"   1. Analise os logs de debug acima")
    print(f"   2. Substitua os CPFs de teste pelos seus CPFs conhecidos")
    print(f"   3. Execute novamente")
    if arquivo_criado:
        print(f"   4. Use o arquivo {arquivo_criado} na interface principal")
