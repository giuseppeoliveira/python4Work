#!/usr/bin/env python3
"""
TESTE RÁPIDO - Execute este script para testar a correção
Substitua o CPF abaixo por um que você sabe que tem códigos
"""

# Teste simples para validar rapidamente
if __name__ == "__main__":
    import sys
    import os
    
    # Adicionar src ao path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    # CPF que você sabe que tem códigos - SUBSTITUA AQUI
    CPF_TESTE = "12345678901"  # ← MUDE ESTE CPF
    
    print("🧪 TESTE RÁPIDO - PARSING XML MELHORADO")
    print("=" * 50)
    print(f"📋 Testando CPF: {CPF_TESTE}")
    print("⚠️  Substitua o CPF acima por um que você sabe que tem códigos!")
    print("=" * 50)
    
    try:
        from obter_divida_cpf import consultar_easycollector, LOGIN_FIXO, SENHA_FIXO
        
        if not LOGIN_FIXO or not SENHA_FIXO:
            print("❌ Credenciais não encontradas no .env")
            exit(1)
            
        print(f"✅ Credenciais OK: {LOGIN_FIXO[:3]}***")
        print(f"🔍 Consultando...")
        
        # Fazer consulta
        id_cliente, id_acordo, datas = consultar_easycollector(CPF_TESTE, LOGIN_FIXO, SENHA_FIXO)
        
        print(f"\n📊 RESULTADO:")
        print(f"   IdCliente: {id_cliente}")
        print(f"   IdAcordo: {id_acordo}")
        print(f"   Datas: {len(datas)} encontradas")
        
        if id_cliente != 0 or id_acordo != 0:
            print(f"\n✅ SUCESSO! Códigos encontrados!")
            print(f"🎉 O problema foi resolvido!")
        else:
            print(f"\n⚠️  Nenhum código encontrado.")
            print(f"   Verifique se o CPF está correto.")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("Verifique credenciais e conexão.")
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
