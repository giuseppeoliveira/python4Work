# 🔧 Python4Work - Interface Unificada

Uma solução completa que centraliza todas as ferramentas do projeto em uma única interface amigável.

## 🚀 **Nova Interface Unificada**

Agora você pode acessar todas as 4 funcionalidades através de uma única aplicação:

- 📋 **Consultar Acordo**
- 🔍 **Obter Dívida por CPF** 
- 📄 **Extrair JSON do Corpo Requisição**
- 📁 **Conversor CSV → XLSX**

### ✨ **Características da Nova Interface:**

- ✅ **Interface única** para todas as funcionalidades
- ✅ **Geração automática de modelos XLSX** para cada função
- ✅ **Escolha do local para salvar** antes de processar
- ✅ **Barra de progresso** em tempo real
- ✅ **Controles de parar/cancelar** durante o processamento
- ✅ **Tratamento de erros** robusto
- ✅ **Threading** para não travar a interface

---

## ⚙️ **Instalação e Configuração**

### 1. **Configurar Variáveis de Ambiente**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com suas credenciais
# LOGIN=seu_login
# SENHA=sua_senha  
# URL=sua_url_consultar_acordo
# URL_DIVIDA=sua_url_obter_divida
```

### 2. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 3. **Executar a Interface**
```bash
python interface_unificada.py
```

---

## 📋 **Como Usar Cada Funcionalidade**

### 🔹 **1. Consultar Acordo**

**Objetivo:** Consulta o status de acordos usando `cod_cliente` e `cod_acordo`

**Fluxo:**
1. Clique em "📋 1. Consultar Acordo"
2. Salve o modelo XLSX gerado automaticamente
3. Preencha as colunas `cod_cliente` e `cod_acordo` no modelo
4. Selecione o arquivo preenchido
5. Escolha onde salvar o resultado
6. A coluna `status_acordo` será preenchida automaticamente

**Colunas do Modelo:**
- `cod_cliente` *(preencher)*
- `cod_acordo` *(preencher)*
- `status_acordo` *(será preenchido)*

---

### 🔹 **2. Obter Dívida por CPF**

**Objetivo:** Obtém informações de dívida ativa usando CPF

**Fluxo:**
1. Clique em "🔍 2. Obter Dívida por CPF"
2. Salve o modelo XLSX gerado automaticamente
3. Preencha a coluna `cpf` no modelo
4. Selecione o arquivo preenchido
5. Escolha onde salvar o resultado
6. As colunas de resultado serão preenchidas automaticamente

**Colunas do Modelo:**
- `cpf` *(preencher)*
- `cod_cliente` *(será preenchido)*
- `cod_acordo` *(será preenchido)*
- `status` *(será preenchido)*
- `observacao` *(será preenchido)*
- `data_vencimento` *(será preenchido)*

---

### 🔹 **3. Extrair JSON do Corpo Requisição**

**Objetivo:** Extrai dados estruturados de campos JSON

**Fluxo:**
1. Clique em "📄 3. Extrair JSON"
2. Salve o modelo XLSX gerado automaticamente
3. Preencha a coluna `corpo_requisicao` com dados JSON
4. Selecione o arquivo preenchido
5. Escolha onde salvar o resultado
6. Os dados JSON serão extraídos e estruturados

**Colunas do Modelo:**
- `corpo_requisicao` *(preencher com JSON)*
- `data_hora` *(opcional)*

**Colunas do Resultado:**
- `idCarga`
- `origem`
- `nmArquivo`
- `data_hora`

---

### 🔹 **4. Conversor CSV → XLSX**

**Objetivo:** Converte arquivos CSV para formato Excel

**Fluxo:**
1. Clique em "📁 4. Converter CSV → XLSX"
2. Selecione os arquivos CSV que deseja converter
3. Escolha a pasta onde salvar os arquivos XLSX
4. Os arquivos serão convertidos automaticamente

**Características:**
- ✅ Detecção automática de delimitadores (`;`, `,`, `tab`)
- ✅ Limpeza automática de cabeçalhos
- ✅ Conversão em lote
- ✅ Log de erros automático

---

## 🛡️ **Segurança**

- ✅ **Credenciais protegidas** via arquivo `.env`
- ✅ **Não exposição** de dados sensíveis no GitHub
- ✅ **Validação** de variáveis de ambiente
- ✅ **Logs seguros** sem credenciais

---

## 🔧 **Controles da Interface**

### **Durante o Processamento:**
- ⏸️ **Parar:** Para o processo salvando o progresso atual
- ❌ **Cancelar:** Cancela o processo sem salvar
- 🔙 **Voltar ao Menu:** Retorna à tela principal

### **Informações em Tempo Real:**
- 📊 **Barra de progresso** visual
- 📈 **Contador** de itens processados
- ⏱️ **Status** da operação atual

---

## 📁 **Estrutura do Projeto**
```
python4Work/
├── interface_unificada.py      # ← NOVA INTERFACE PRINCIPAL
├── consultar_acordo.py         # Script original (ainda funciona)
├── obter_divida_cpf.py         # Script original (ainda funciona)
├── extrair_json_corpo_requisicao.py
├── conversor_csv_xlsx.py
├── .env                        # Suas credenciais (não vai pro GitHub)
├── .env.example                # Template
├── .gitignore                  # Proteção de arquivos
├── requirements.txt            # Dependências
├── SECURITY.md                 # Instruções de segurança
└── README_UNIFICADO.md         # Este arquivo
```

---

## 🎯 **Vantagens da Nova Interface**

### **Para o Usuário:**
- ✅ **Simplicidade:** Uma única aplicação para tudo
- ✅ **Orientação:** Modelos automáticos guiam o uso
- ✅ **Controle:** Pode parar/cancelar a qualquer momento
- ✅ **Feedback:** Progresso em tempo real

### **Para Manutenção:**
- ✅ **Código centralizado:** Mais fácil de manter
- ✅ **Reutilização:** Funções compartilhadas
- ✅ **Consistência:** Interface padronizada
- ✅ **Extensibilidade:** Fácil adicionar novas funcionalidades

---

## 🚀 **Próximos Passos**

1. **Execute:** `python interface_unificada.py`
2. **Teste cada funcionalidade** com os modelos gerados
3. **Mantenha:** Os scripts originais ainda funcionam se preferir

---

## 📞 **Suporte**

- 📖 **Documentação:** Este README
- 🛡️ **Segurança:** Ver `SECURITY.md`
- 🐛 **Bugs:** Verifique os logs gerados automaticamente
- ⚙️ **Configuração:** Verifique o arquivo `.env`

---

**🎉 Aproveite a nova experiência unificada do Python4Work!**
