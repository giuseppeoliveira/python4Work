#!/usr/bin/env python3
"""
Teste específico para validar a correção do problema de parsing XML
Execute este script com um CPF que você sabe que possui cod_acordo e cod_cliente
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def testar_parsing_xml_detalhado():
    """
    Teste detalhado do parsing XML com um CPF específico
    """
    
    print("🔬 TESTE DETALHADO - PARSING XML MELHORADO")
    print("=" * 70)
    
    # ⚠️ SUBSTITUA ESTE CPF POR UM QUE VOCÊ SABE QUE TEM CÓDIGOS
    CPF_TESTE = "12345678901"  # ← MUDE AQUI para um CPF real que você testou manualmente
    
    print(f"📋 CPF sendo testado: {CPF_TESTE}")
    print("⚠️  IMPORTANTE: Substitua pelo CPF que você consultou manualmente!")
    print("=" * 70)
    
    try:
        from obter_divida_cpf import consultar_easycollector, LOGIN_FIXO, SENHA_FIXO
        
        print(f"✅ Credenciais carregadas: {LOGIN_FIXO[:3] if LOGIN_FIXO else 'NÃO'}***")
        print(f"🔍 Iniciando consulta detalhada para CPF {CPF_TESTE}...")
        print("\n" + "="*50 + " EXECUTANDO CONSULTA " + "="*50)
        
        # Fazer a consulta com debug detalhado
        id_cliente, id_acordo, datas = consultar_easycollector(CPF_TESTE, LOGIN_FIXO, SENHA_FIXO)
        
        print("\n" + "="*50 + " RESULTADOS FINAIS " + "="*50)
        print(f"📊 RESULTADOS DA CONSULTA:")
        print(f"   • IdCliente: {id_cliente}")
        print(f"   • IdAcordo: {id_acordo}")
        print(f"   • Quantidade de datas: {len(datas)}")
        
        if datas:
            print(f"   • Primeiras datas: {datas[:5]}")
        
        # Verificar se encontrou os códigos
        if id_cliente != 0 or id_acordo != 0:
            print("\n✅ SUCESSO! A implementação melhorada encontrou os códigos!")
            print("🎉 O problema foi RESOLVIDO!")
            
            if id_cliente != 0:
                print(f"   ✓ IdCliente encontrado: {id_cliente}")
            if id_acordo != 0:
                print(f"   ✓ IdAcordo encontrado: {id_acordo}")
                
        else:
            print("\n⚠️  ATENÇÃO: Ainda não encontrou os códigos...")
            print("💡 Possíveis causas:")
            print("   1. CPF de teste não possui códigos reais")
            print("   2. Problema de conectividade ou credenciais")
            print("   3. Estrutura do XML diferente do esperado")
            print("\n📝 Verifique os logs de DEBUG acima para mais detalhes")
        
        # Simular processamento completo da linha
        print(f"\n" + "="*50 + " TESTE PROCESSAMENTO COMPLETO " + "="*50)
        
        from obter_divida_cpf import processar_linha_cpf
        
        row_data = (0, {
            'cpf': CPF_TESTE,
            'cod_cliente': '0',
            'cod_acordo': '0'
        })
        
        i, status, observacao, new_cod_cliente, new_cod_acordo = processar_linha_cpf(row_data)
        
        print(f"📋 RESULTADO DO PROCESSAMENTO COMPLETO:")
        print(f"   • Status: {status}")
        print(f"   • Observação: {observacao}")
        print(f"   • Novo cod_cliente: {new_cod_cliente}")
        print(f"   • Novo cod_acordo: {new_cod_acordo}")
        
        return {
            'cpf': CPF_TESTE,
            'id_cliente': id_cliente,
            'id_acordo': id_acordo,
            'datas_count': len(datas),
            'status': status,
            'observacao': observacao,
            'new_cod_cliente': new_cod_cliente,
            'new_cod_acordo': new_cod_acordo,
            'sucesso': id_cliente != 0 or id_acordo != 0
        }
        
    except Exception as e:
        print(f"❌ ERRO DURANTE O TESTE: {e}")
        print(f"📝 Verifique:")
        print(f"   1. Arquivo .env com LOGIN e SENHA corretos")
        print(f"   2. Conexão com internet")
        print(f"   3. Se a API está funcionando")
        return {
            'cpf': CPF_TESTE,
            'erro': str(e),
            'sucesso': False
        }

def criar_arquivo_teste_xml():
    """
    Cria um arquivo Excel de teste com 3 CPFs para validação
    """
    print(f"\n📄 CRIANDO ARQUIVO DE TESTE PARA VALIDAÇÃO...")
    
    # Criar dados de teste - SUBSTITUA pelos seus CPFs conhecidos
    dados_teste = [
        {
            "cpf": "12345678901",  # ← Substitua por CPF real
            "nome": "Teste XML Parsing 1",
            "cod_cliente": "0",
            "cod_acordo": "0",
            "status": "",
            "observacao": ""
        },
        {
            "cpf": "98765432100",  # ← Substitua por CPF real
            "nome": "Teste XML Parsing 2", 
            "cod_cliente": "0",
            "cod_acordo": "0",
            "status": "",
            "observacao": ""
        },
        {
            "cpf": "11111111111",  # ← Substitua por CPF real
            "nome": "Teste XML Parsing 3",
            "cod_cliente": "0", 
            "cod_acordo": "0",
            "status": "",
            "observacao": ""
        }
    ]
    
    df = pd.DataFrame(dados_teste)
    arquivo_teste = f"teste_xml_parsing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        df.to_excel(arquivo_teste, index=False)
        print(f"✅ Arquivo criado: {arquivo_teste}")
        print(f"📋 Próximos passos:")
        print(f"   1. Substitua os CPFs pelos que você sabe que têm códigos")
        print(f"   2. Use este arquivo na interface principal")
        print(f"   3. Verifique se os códigos são capturados corretamente")
        return arquivo_teste
    except Exception as e:
        print(f"❌ Erro ao criar arquivo: {e}")
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO VALIDAÇÃO DO PARSING XML MELHORADO")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Executar teste detalhado
    resultado = testar_parsing_xml_detalhado()
    
    # Criar arquivo de teste
    arquivo_criado = criar_arquivo_teste_xml()
    
    print(f"\n" + "="*70)
    print("🏁 VALIDAÇÃO CONCLUÍDA!")
    print(f"📊 Resultado: {'✅ SUCESSO' if resultado.get('sucesso') else '⚠️ NECESSITA AJUSTES'}")
    
    if resultado.get('sucesso'):
        print(f"🎉 A implementação melhorada está funcionando!")
        print(f"   • IdCliente capturado: {resultado.get('id_cliente')}")
        print(f"   • IdAcordo capturado: {resultado.get('id_acordo')}")
    else:
        print(f"🔧 Ajustes podem ser necessários baseados nos logs acima")
    
    print(f"\n📝 Próximos passos:")
    print(f"   1. Substitua os CPFs de teste pelos reais")
    print(f"   2. Execute este teste novamente")
    print(f"   3. Use o arquivo {arquivo_criado} na interface")
    print(f"=" * 70)
