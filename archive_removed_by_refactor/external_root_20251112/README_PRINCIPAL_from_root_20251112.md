# 🐍 Python4Work - Suite de Ferramentas

Repositório com ferramentas úteis para automação de trabalho.

## 📦 Aplicações Disponíveis

### 1. 🔧 Python4Work (Aplicação Principal)
Interface com múltiplas ferramentas:
- Conversor CSV para XLSX
- Consulta de acordos
- Filtro de duplicatas
- Extração de JSON
- E muito mais...

**Como executar:**
- Duplo clique em: `INICIAR_PYTHON4WORK.bat`
- Ou terminal: `python main.py`

---

### 2. 🛡️ NoLogout (Prevenção de Logout)
Mantém sua sessão Windows ativa para evitar deslogar por inatividade.

**Como executar:**
- Duplo clique em: `Nologout\INICIAR.bat`
- Ou terminal: `cd Nologout` e `python nologout_gui.py`

**Documentação completa:** `Nologout\README.md`

---

## 🚀 Início Rápido

### Método 1: Arquivos BAT (Mais Fácil)
1. **Python4Work**: Duplo clique em `INICIAR_PYTHON4WORK.bat`
2. **NoLogout**: Duplo clique em `Nologout\INICIAR.bat`

### Método 2: Terminal PowerShell
```powershell
# Para Python4Work
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work"
python main.py

# Para NoLogout
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nologout"
python nologout_gui.py
```

---

## 📋 Comandos Úteis

Veja o arquivo **`COMANDOS_EXECUCAO.md`** para guia completo de comandos!

---

## 📁 Estrutura do Projeto

```
Python4Work/
├── main.py                          # Aplicação principal
├── INICIAR_PYTHON4WORK.bat         # Atalho Python4Work
├── COMANDOS_EXECUCAO.md            # Guia de comandos
├── requirements.txt                # Dependências
├── config.json                     # Configurações
├── core/                           # Módulos principais
├── interfaces/                     # Interfaces gráficas
├── src/                            # Ferramentas
├── data/                           # Dados
├── logs/                           # Logs
└── Nologout/                       # Aplicação NoLogout
    ├── nologout_gui.py             # Interface NoLogout
    ├── INICIAR.bat                 # Atalho NoLogout
    ├── README.md                   # Docs NoLogout
    └── ...
```

---

## 🛠️ Instalação de Dependências

### Python4Work
```powershell
pip install -r requirements.txt
```

### NoLog
```powershell
cd Nolog
pip install -r requirements.txt
```

---

## 💡 Dicas

- Use os arquivos `.bat` para iniciar mais facilmente
- Consulte `COMANDOS_EXECUCAO.md` para ajuda com terminal
- Cada aplicação tem seu próprio README com detalhes

---

## 📝 Licença

Uso pessoal e profissional.
