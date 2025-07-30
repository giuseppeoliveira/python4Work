#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

def criar_modelos():
    """Cria os modelos Excel para cada funcionalidade"""
    
    # Pasta dos modelos
    modelos_dir = 'Modelos'
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
    
    print("🔧 Criando modelos Excel...")
    
    # 1. Modelo para Consultar Acordo
    dados_acordo = {
        'cod_cliente': ['123456', '789012'],
        'cod_acordo': ['AC001', 'AC002'],
        'observacoes': ['Exemplo cliente 1', 'Exemplo cliente 2']
    }
    df_acordo = pd.DataFrame(dados_acordo)
    arquivo_acordo = f'{modelos_dir}/modelo_consultar_acordo.xlsx'
    df_acordo.to_excel(arquivo_acordo, index=False)
    print(f"✅ {arquivo_acordo}")
    
    # 2. Modelo para Obter Dívida CPF
    dados_cpf = {
        'cpf': ['12345678901', '98765432100'],
        'nome': ['João Silva', 'Maria Santos'],
        'observacoes': ['Exemplo CPF 1', 'Exemplo CPF 2']
    }
    df_cpf = pd.DataFrame(dados_cpf)
    arquivo_cpf = f'{modelos_dir}/modelo_obter_divida_cpf.xlsx'
    df_cpf.to_excel(arquivo_cpf, index=False)
    print(f"✅ {arquivo_cpf}")
    
    # 3. Modelo para Extrair JSON
    dados_json = {
        'corpo_requisicao': [
            '{"usuario": "exemplo1", "dados": "teste1"}',
            '{"usuario": "exemplo2", "dados": "teste2"}'
        ],
        'tipo_operacao': ['consulta', 'insercao'],
        'observacoes': ['Exemplo JSON 1', 'Exemplo JSON 2']
    }
    df_json = pd.DataFrame(dados_json)
    arquivo_json = f'{modelos_dir}/modelo_extrair_json.xlsx'
    df_json.to_excel(arquivo_json, index=False)
    print(f"✅ {arquivo_json}")
    
    # 4. Modelo para Converter CSV
    dados_csv = {
        'campo1': ['valor1', 'valor2'],
        'campo2': ['valor3', 'valor4'],
        'campo3': ['valor5', 'valor6']
    }
    df_csv = pd.DataFrame(dados_csv)
    arquivo_csv = f'{modelos_dir}/modelo_converter_csv.xlsx'
    df_csv.to_excel(arquivo_csv, index=False)
    print(f"✅ {arquivo_csv}")
    
    print("🎉 Todos os modelos criados com sucesso!")

if __name__ == "__main__":
    criar_modelos()
