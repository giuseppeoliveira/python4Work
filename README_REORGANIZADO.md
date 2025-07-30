# Python4Work - Projeto Reorganizado

Este projeto foi reorganizado para seguir uma estrutura mais profissional e organizada.

## 📁 Estrutura do Projeto

```
python4Work/
├── 📋 main.py                    # Launcher - Interface Profissional
├── 📋 main_unified.py            # Launcher - Interface Unificada
├── 📋 config.json                # Configurações do sistema
├── 📋 requirements.txt           # Dependências Python
├── 📋 .env                       # Variáveis de ambiente
├── 📋 .env.example               # Exemplo de variáveis de ambiente
├── 📋 Readme.md                  # Este arquivo
│
├── 🏗️ core/                      # Componentes centrais do sistema
│   ├── config_manager.py         # Gerenciamento de configurações
│   ├── professional_logger.py    # Sistema de logging profissional
│   ├── theme_manager.py          # Gerenciamento de temas visuais
│   └── data_validator.py         # Validação de dados
│
├── 🖥️ interfaces/                # Interfaces gráficas
│   ├── interface_profissional.py # Interface profissional (recomendada)
│   ├── interface_unificada.py    # Interface unificada simples
│   └── teste_interface.py        # Script de teste
│
├── ⚙️ src/                       # Funcionalidades principais
│   ├── consultar_acordo.py       # Consulta status de acordos
│   ├── obter_divida_cpf.py       # Consulta dívidas por CPF
│   ├── extrair_json_corpo_requisicao.py # Extrai JSON de requisições
│   └── conversor_csv_xlsx.py     # Converte CSV para XLSX
│
├── 📊 data/                      # Dados e modelos
│   ├── Modelos/                  # Templates Excel
│   │   ├── modelo_consultar_acordo.xlsx
│   │   ├── modelo_obter_divida_cpf.xlsx
│   │   ├── modelo_extrair_json.xlsx
│   │   └── modelo_converter_csv.xlsx
│   └── logs/                     # Logs do sistema
│       ├── python4workpro.log
│       ├── python4workpro_errors.log
│       └── sessions/             # Logs de sessão
│
├── 📚 docs/                      # Documentação
│   ├── README_PROFISSIONAL.md
│   ├── README_UNIFICADO.md
│   ├── MELHORIAS_PROFISSIONAIS.md
│   └── SECURITY.md
│
└── 🗂️ legacy/                    # Scripts auxiliares
    └── criar_modelos.py          # Gerador de modelos Excel
```

## 🚀 Como Usar

### Interface Profissional (Recomendada)
```bash
python main.py
```

### Interface Unificada (Simples)
```bash
python main_unified.py
```

### Funcionalidades Individuais
```bash
# Consultar acordos
python src/consultar_acordo.py

# Obter dívidas por CPF
python src/obter_divida_cpf.py

# Extrair JSON
python src/extrair_json_corpo_requisicao.py

# Converter CSV para XLSX
python src/conversor_csv_xlsx.py
```

## 📋 Pré-requisitos

1. **Python 3.8+**
2. **Dependências** (instalar com `pip install -r requirements.txt`):
   - tkinter (geralmente incluído com Python)
   - pandas
   - requests
   - beautifulsoup4
   - python-dotenv
   - openpyxl
   - lxml

## ⚙️ Configuração

1. **Configurar variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Editar o arquivo .env com suas credenciais
   ```

2. **Personalizar configurações:**
   - Editar `config.json` para ajustar temas, comportamentos e parâmetros do sistema

## 🌟 Características Profissionais

### Interface Profissional
- ✅ Sistema de logging estruturado
- ✅ Validação robusta de dados  
- ✅ Múltiplos temas visuais
- ✅ Configurações avançadas
- ✅ Relatórios detalhados
- ✅ Sistema de sessões
- ✅ Backup automático

### Interface Unificada
- ✅ Interface simples e direta
- ✅ Todas as funcionalidades em um só lugar
- ✅ Ideal para uso básico

## 🔧 Melhorias da Reorganização

### ✅ Estrutura Organizada
- Arquivos agrupados por categoria e função
- Separação clara entre core, interfaces e funcionalidades
- Documentação centralizada

### ✅ Facilidade de Manutenção
- Imports corrigidos e organizados
- Modularização melhorada
- Scripts de inicialização dedicados

### ✅ Escalabilidade
- Estrutura preparada para crescimento
- Componentes independentes
- Sistema modular

## 📝 Logs e Monitoramento

O sistema profissional gera logs detalhados em:
- `data/logs/python4workpro.log` - Log geral
- `data/logs/python4workpro_errors.log` - Log de erros
- `data/logs/sessions/` - Logs de sessão individual

## 🔐 Segurança

- Variáveis sensíveis em arquivo `.env`
- Logs de auditoria completos
- Validação de dados de entrada
- Tratamento robusto de erros

## 🚀 Próximos Passos

1. **Desenvolvimento:** Adicionar novas funcionalidades na pasta `src/`
2. **Interfaces:** Criar novas interfaces na pasta `interfaces/`
3. **Core:** Expandir componentes centrais na pasta `core/`
4. **Documentação:** Atualizar documentação na pasta `docs/`

---

**Versão:** 2.0.0 Professional  
**Status:** ✅ Reorganizado e Funcional  
**Última Atualização:** $(Get-Date -Format "dd/MM/yyyy HH:mm")
