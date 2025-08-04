#!/usr/bin/env python3
"""
TESTE ESPECÍFICO - Validação dos delimitadores NmCedente/PercentualDescontoJuros
Execute este script para testar a nova lógica de parsing baseada nos delimitadores específicos
"""

import sys
import os
from datetime import datetime

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def testar_delimitadores_especificos():
    """
    Teste específico da nova lógica de delimitadores
    """
    
    print("🎯 TESTE DOS DELIMITADORES ESPECÍFICOS")
    print("=" * 60)
    print("Testando nova lógica: <NmCedente> até </PercentualDescontoJuros>")
    print("=" * 60)
    
    # CPF de teste - SUBSTITUA por um real
    CPF_TESTE = "12345678901"  # ← MUDE AQUI
    
    print(f"📋 CPF sendo testado: {CPF_TESTE}")
    print("⚠️  IMPORTANTE: Substitua pelo CPF que você testou manualmente!")
    
    try:
        from obter_divida_cpf import consultar_easycollector, LOGIN_FIXO, SENHA_FIXO
        
        if not LOGIN_FIXO or not SENHA_FIXO:
            print("❌ Credenciais não encontradas no .env")
            return
        
        print(f"✅ Credenciais OK: {LOGIN_FIXO[:3]}***")
        print(f"\n🔍 Executando consulta com nova lógica de delimitadores...")
        print("=" * 60)
        
        # A função já tem debug interno para os primeiros CPFs
        id_cliente, id_acordo, datas = consultar_easycollector(CPF_TESTE, LOGIN_FIXO, SENHA_FIXO)
        
        print("=" * 60)
        print("📊 RESULTADO FINAL DA NOVA LÓGICA:")
        print(f"   • IdCliente: {id_cliente}")
        print(f"   • IdAcordo: {id_acordo}")
        print(f"   • Datas encontradas: {len(datas)}")
        
        if datas:
            print(f"   • Primeira data: {datas[0]}")
            if len(datas) > 1:
                print(f"   • Última data: {datas[-1]}")
        
        print("=" * 60)
        
        # Avaliação do resultado
        if id_cliente != 0 and id_acordo != 0:
            print("🎉 EXCELENTE! Ambos os códigos foram encontrados!")
            print(f"   ✅ IdCliente: {id_cliente}")
            print(f"   ✅ IdAcordo: {id_acordo}")
            resultado = "SUCESSO_COMPLETO"
        elif id_cliente != 0 or id_acordo != 0:
            print("✅ PARCIAL! Pelo menos um código foi encontrado!")
            if id_cliente != 0:
                print(f"   ✅ IdCliente: {id_cliente}")
            if id_acordo != 0:
                print(f"   ✅ IdAcordo: {id_acordo}")
            resultado = "SUCESSO_PARCIAL"
        else:
            print("⚠️  Nenhum código encontrado.")
            print("   Possíveis causas:")
            print("   1. CPF não possui dados reais")
            print("   2. Problema de conectividade")
            print("   3. Estrutura XML diferente do esperado")
            resultado = "SEM_RESULTADOS"
        
        return {
            'cpf': CPF_TESTE,
            'id_cliente': id_cliente,
            'id_acordo': id_acordo,
            'datas_count': len(datas),
            'resultado': resultado,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return {
            'cpf': CPF_TESTE,
            'erro': str(e),
            'resultado': "ERRO",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def simular_xml_parsing():
    """
    Simula o parsing de um XML exemplo baseado nos delimitadores
    """
    
    print(f"\n🧪 SIMULAÇÃO DE PARSING XML")
    print("=" * 60)
    
    # XML exemplo baseado no que você forneceu
    xml_exemplo = """
    <root>
    <NmCedente>FICOU FACIL - CARTEIRA</NmCedente>
    <idProduto>224</idProduto>
    <IdCliente>6778571</IdCliente>
    <IdAcordo>163993595</IdAcordo>
    <DataVencimento>2025-08-31T00:00:00</DataVencimento>
    </PercentualDescontoJuros>
    
    <NmCedente>OUTRO CEDENTE</NmCedente>
    <idProduto>225</idProduto>
    <IdCliente>1234567</IdCliente>
    <IdAcordo>987654321</IdAcordo>
    <DataVencimento>2025-09-15T00:00:00</DataVencimento>
    </PercentualDescontoJuros>
    </root>
    """
    
    print("📋 XML de exemplo:")
    print(xml_exemplo)
    
    # Simular parsing
    blocos = []
    if "<NmCedente>" in xml_exemplo and "</PercentualDescontoJuros>" in xml_exemplo:
        partes = xml_exemplo.split("<NmCedente>")
        for i, parte in enumerate(partes[1:], 1):
            if "</PercentualDescontoJuros>" in parte:
                fim_bloco = parte.find("</PercentualDescontoJuros>") + len("</PercentualDescontoJuros>")
                bloco_completo = "<NmCedente>" + parte[:fim_bloco]
                blocos.append(bloco_completo)
                print(f"\n📦 Bloco {i} extraído:")
                print(f"   Início: <NmCedente>")
                print(f"   Fim: </PercentualDescontoJuros>")
                print(f"   Tamanho: {len(bloco_completo)} caracteres")
    
    print(f"\n✅ Total de blocos extraídos: {len(blocos)}")
    print("🎯 A nova lógica deve conseguir processar cada bloco individualmente!")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE DOS DELIMITADORES ESPECÍFICOS")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Simular parsing primeiro
    simular_xml_parsing()
    
    # Teste real
    resultado = testar_delimitadores_especificos()
    
    print(f"\n🏁 TESTE CONCLUÍDO!")
    print(f"📊 Resultado: {resultado.get('resultado', 'DESCONHECIDO')}")
    
    if resultado.get('resultado') in ['SUCESSO_COMPLETO', 'SUCESSO_PARCIAL']:
        print(f"🎉 A nova lógica de delimitadores está funcionando!")
    elif resultado.get('resultado') == 'SEM_RESULTADOS':
        print(f"🔧 Teste inconclusivo - verifique se o CPF possui dados reais")
    else:
        print(f"⚠️  Possível problema - verifique logs acima")
        
    print(f"\n📝 Próximos passos:")
    print(f"   1. Substitua o CPF por um real que você sabe que tem códigos")
    print(f"   2. Execute novamente: python teste_delimitadores.py")
    print(f"   3. Observe os logs detalhados da nova lógica")
    print(f"   4. Use a interface principal se o teste for bem-sucedido")
