# 🚀 **Python4Work - Ferramenta Profissional de Automação**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Interface](https://img.shields.io/badge/Interface-Professional-green.svg)](interface_profissional.py)
[![Status](https://img.shields.io/badge/Status-Enterprise%20Ready-brightgreen.svg)]()
[![Security](https://img.shields.io/badge/Security-Protected-red.svg)]()

**🎯 Solução empresarial para automação de consultas e processamento de dados**

---

## 🌟 **Destaques da Versão Profissional**

- 🖥️ **Interface moderna unificada** com 4 funcionalidades integradas
- 📊 **Sistema de logging profissional** com rastreamento de sessões
- ⚙️ **Configurações dinâmicas** via JSON
- 🎨 **4 temas profissionais** (Moderno, Escuro, Corporativo, Natureza)
- 🔐 **Segurança aprimorada** com auditoria
- 📈 **Monitoramento** completo de sessões
- 🛡️ **Sistema de backup** automático

---

## ⚙️ **Configuração Inicial**

### 1. **Configurar Variáveis de Ambiente**

Copie e configure o arquivo de credenciais:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
LOGIN=seu_login_aqui
SENHA=sua_senha_aqui
URL=sua_url_consultar_acordo_aqui
URL_DIVIDA=sua_url_obter_divida_aqui
```

### 2. **Instalar Dependências**

Execute o comando:
```bash
pip install -r requirements.txt
```

---

## 🎯 **Funcionalidades Integradas**

A interface profissional oferece **4 funcionalidades** em uma única aplicação:

### 📋 **1. Consultar Acordo**
- Consulta status de acordos usando `cod_cliente` e `cod_acordo`
- Modelo XLSX gerado automaticamente
- Validação robusta de dados

### 🔍 **2. Obter Dívida por CPF**
- Obtém informações de dívida ativa por CPF
- Validação de CPF com dígitos verificadores
- Detecção automática de duplicatas

### 📄 **3. Extrair JSON**
- Extrai dados estruturados de campos JSON
- Processa `corpo_requisicao` complexos
- Estrutura dados automaticamente

### 📁 **4. Converter CSV → XLSX**
- Converte múltiplos arquivos CSV
- Detecção automática de delimitadores
- Validação e limpeza de dados

---

## 💻 **Como Usar**

### **🌟 Versão Profissional (Recomendada):**
```bash
python interface_profissional.py
```

### **📋 Versão Unificada (Alternativa):**
```bash
python interface_unificada.py
```

### **⚙️ Scripts Individuais (Legado):**
```bash
# Para usar scripts originais separadamente
python consultar_acordo.py
python obter_divida_cpf.py
python extrair_json_corpo_requisicao.py
python conversor_csv_xlsx.py
```

---

## 🔧 **Configurações Avançadas**

### **Arquivo `config.json` (criado automaticamente):**
```json
{
  "app": {
    "theme": "modern",
    "auto_backup": true,
    "backup_interval": 10,
    "max_retries": 3
  },
  "ui": {
    "window_width": 1000,
    "window_height": 700,
    "confirm_exit": true
  },
  "logging": {
    "level": "INFO",
    "max_file_size_mb": 10,
    "detailed_errors": true
  }
}
```

### **Temas Disponíveis:**
- 🌟 **modern:** Cores suaves e modernas (padrão)
- 🌙 **dark:** Tema escuro para reduzir cansaço visual
- 🏢 **corporate:** Profissional para ambiente corporativo
- 🌿 **nature:** Inspirado em tons verdes

---

## 📊 **Sistema de Monitoramento**

### **Logs Estruturados:**
```
logs/
├── python4workpro.log              # Log principal
├── python4workpro_errors.log       # Apenas erros
└── sessions/
    └── session_abc123_timestamp.json   # Relatórios por sessão
```

### **Informações Monitoradas:**
- ✅ Operações executadas com timestamps
- ✅ Erros detalhados com stack traces
- ✅ Ações do usuário para auditoria
- ✅ Chamadas de API com status
- ✅ Performance e métricas de uso

---

## ✅ **Validação Profissional de Dados**

### **Validações Implementadas:**
- 🆔 **CPF:** Validação completa com dígitos verificadores
- 🔢 **Códigos:** Validação de range e formato
- 📅 **Datas:** Validação de formato e consistência
- 📧 **Emails:** Validação de formato (quando aplicável)
- 🔄 **Duplicatas:** Detecção automática

### **Relatórios de Validação:**
- ❌ **Erros críticos:** Impedem processamento
- ⚠️ **Avisos:** Dados suspeitos mas processáveis
- ℹ️ **Informações:** Estatísticas e resumos

---

## 🛡️ **Segurança**

### **Características de Segurança:**
- 🔐 **Credenciais protegidas** via arquivo `.env`
- 🚫 **Não exposição** de dados sensíveis no GitHub
- 📝 **Logs mascarados** para senhas e dados sensíveis
- 🔍 **Auditoria completa** de ações do usuário
- ✅ **Validação SSL** configurável

### **Arquivos Protegidos:**
- `.env` (suas credenciais) - **nunca vai para o GitHub**
- `logs/` (dados de sessão) - incluído no `.gitignore`
- Dados temporários e cache

---

## 📁 **Estrutura do Projeto**

```
python4Work/
├── 🚀 interface_profissional.py      # Interface principal (USAR ESTE!)
├── 📋 interface_unificada.py          # Interface alternativa
├── 📊 consultar_acordo.py             # Script individual
├── 🔍 obter_divida_cpf.py             # Script individual
├── 📄 extrair_json_corpo_requisicao.py
├── 📁 conversor_csv_xlsx.py
├── ⚙️ config_manager.py               # Sistema de configuração
├── 📝 professional_logger.py          # Sistema de logging
├── ✅ data_validator.py               # Sistema de validação
├── 🎨 theme_manager.py                # Sistema de temas
├── 🔐 .env                           # Suas credenciais (protegido)
├── 📋 .env.example                   # Template de credenciais
├── 🛡️ .gitignore                     # Proteção de arquivos
├── 📦 requirements.txt               # Dependências
├── ⚙️ config.json                    # Configurações (auto-criado)
├── 📚 MELHORIAS_PROFISSIONAIS.md     # Guia de melhorias
├── 🔒 SECURITY.md                    # Instruções de segurança
└── 📝 logs/                          # Logs estruturados
```

---

## 🆘 **Solução de Problemas**

### **Problemas Comuns:**

1. **"Variáveis de ambiente não encontradas"**
   ```bash
   cp .env.example .env
   # Edite o .env com suas credenciais
   ```

2. **"Erro de importação"**
   ```bash
   pip install -r requirements.txt
   ```

3. **"Interface não abre"**
   ```bash
   python interface_profissional.py
   # Verifique logs em logs/python4workpro_errors.log
   ```

4. **"Validação de CPF falha"**
   - CPF deve ter 11 dígitos
   - Dígitos verificadores devem estar corretos
   - Verifique relatório de validação

### **Logs para Debug:**
- **Geral:** `logs/python4workpro.log`
- **Erros:** `logs/python4workpro_errors.log`
- **Sessões:** `logs/sessions/`

---

## 📈 **Changelog - Versão 2.0**

### **🆕 Novidades:**
- ✅ Interface profissional unificada
- ✅ Sistema de logging estruturado
- ✅ Configurações dinâmicas via JSON
- ✅ 4 temas visuais profissionais
- ✅ Validação robusta com CPF
- ✅ Monitoramento de sessões
- ✅ Sistema de backup automático
- ✅ Arquitetura modular
- ✅ Documentação profissional

### **🔧 Melhorias:**
- ✅ Performance otimizada com threading
- ✅ Interface responsiva e moderna
- ✅ Tratamento de erros aprimorado
- ✅ Segurança aprimorada
- ✅ Experiência do usuário profissional

---

## 🎯 **Comandos Rápidos**

```bash
# Executar versão profissional
python interface_profissional.py

# Executar versão unificada
python interface_unificada.py

# Ver logs em tempo real
tail -f logs/python4workpro.log

# Verificar configurações
cat config.json

# Verificar status do ambiente
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Configurado' if all([os.getenv('LOGIN'), os.getenv('SENHA')]) else '❌ Faltam credenciais')"
```

---

## 📞 **Suporte e Documentação**

- 📖 **Documentação Completa:** `MELHORIAS_PROFISSIONAIS.md`
- 🔒 **Segurança:** `SECURITY.md`
- 📋 **Interface Unificada:** `README_UNIFICADO.md`
- 🐛 **Problemas:** Verifique `logs/` para detalhes
- ⚙️ **Configuração:** Edite `config.json`

---

## 🏆 **Status do Projeto**

**🎉 PROJETO COMPLETAMENTE PROFISSIONALIZADO!**

- ✅ **Nível Enterprise** - Pronto para produção
- ✅ **Interface Moderna** - Layout profissional
- ✅ **Logging Completo** - Monitoramento total
- ✅ **Configurável** - Personalizações avançadas
- ✅ **Seguro** - Credenciais protegidas
- ✅ **Documentado** - Guias completos
- ✅ **Manutenível** - Arquitetura modular

**🚀 Execute: `python interface_profissional.py` e aproveite sua nova ferramenta profissional!**
