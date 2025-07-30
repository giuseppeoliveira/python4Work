# 🔐 Instruções de Segurança

## ⚠️ IMPORTANTE: Protegendo suas Credenciais

Este projeto foi configurado para manter suas credenciais seguras e não expostas no GitHub. Siga estas instruções:

### ✅ O que está protegido:
- Arquivo `.env` - contém suas credenciais reais (não vai para o GitHub)
- Logs com dados sensíveis (`.gitignore` configurado)

### ✅ Como configurar:
1. **NUNCA** edite diretamente os arquivos `.py` com suas credenciais
2. **SEMPRE** use o arquivo `.env` para suas credenciais
3. Use o arquivo `.env.example` como referência

### ✅ Primeira instalação:
```bash
# 1. Clone o repositório
git clone https://github.com/giuseppeoliveira/python4Work.git

# 2. Copie o arquivo de exemplo
cp .env.example .env

# 3. Edite o arquivo .env com suas credenciais reais
# (use um editor de texto)

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute os scripts normalmente
python consultar_acordo.py
python obter_divida_cpf.py
```

### ❌ O que NÃO fazer:
- ❌ Não commit o arquivo `.env`
- ❌ Não coloque credenciais diretamente no código
- ❌ Não remova o `.env` do `.gitignore`

### 🔍 Verificar se está seguro:
Execute este comando para ver o que será enviado ao GitHub:
```bash
git status
```

O arquivo `.env` NÃO deve aparecer na lista de arquivos para commit.

---

## 🛡️ Arquivos de Segurança Incluídos:

- **.env** - Suas credenciais (não vai para o GitHub)
- **.env.example** - Template sem dados sensíveis
- **.gitignore** - Lista de arquivos que não vão para o GitHub
- **requirements.txt** - Lista de dependências do projeto
