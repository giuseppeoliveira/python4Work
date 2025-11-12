# 🚀 COMANDOS PARA EXECUTAR AS APLICAÇÕES

# 🚀 COMANDOS PARA EXECUTAR AS APLICAÇÕES NO POWERSHELL

## 📂 Estrutura do Repositório

```
Python4Work/                         ← Pasta raiz do repositório
├── python4Work/                     ← Pasta com o código
│   └── main.py                      ← Aplicação Principal (Python4Work)
└── Nolog/                           ← Aplicação NoLog
    └── nolog_gui.py
```

---

## 🟢 PYTHON4WORK (Aplicação Principal)

### ✅ Comando Recomendado
```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work"
python main.py
```

### Ou com caminho completo (de qualquer lugar)
```powershell
python "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work\main.py"
```

### O que faz:
- Interface principal com múltiplas ferramentas
- Conversor CSV/XLSX
- Consulta de acordos
- Filtrar duplicatas
- E outras funcionalidades

---

## 🛡️ NOLOG (Prevenção de Logout)

### ✅ Comando Recomendado
```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nolog"
python nolog_gui.py
```

### Ou com caminho completo (de qualquer lugar)
```powershell
python "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nolog\nolog_gui.py"
```

### O que faz:
- Mantém sua sessão ativa
- Previne logout automático
- Mantém VPN conectada

---

## 📋 RESUMO RÁPIDO - COPIE E COLE

### Python4Work
```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work"; python main.py
```

### NoLog
```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nolog"; python nolog_gui.py
```

---

## ⚡ COMANDOS DE UMA LINHA (Copie e Cole Direto!)

Se você já está em qualquer pasta, pode copiar e colar esses comandos:

### Para Python4Work:
```powershell
Push-Location "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work"; python main.py
```

### Para NoLog:
```powershell
Push-Location "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nolog"; python nolog_gui.py
```

---

## ⚠️ IMPORTANTE - Certifique-se de estar na pasta correta

### Para Python4Work:
```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work"
python main.py
```

### Para NoLog:
```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nolog"
python nolog_gui.py
```

---

## � DICAS ÚTEIS

### 1. Verificar onde você está:
```powershell
pwd
```

### 2. Listar arquivos da pasta atual:
```powershell
ls
```

### 3. Voltar para a pasta anterior:
```powershell
cd ..
```

### 4. Ir direto para o Desktop:
```powershell
cd ~\Desktop
```

### 5. Limpar a tela do terminal:
```powershell
cls
```

---

## 🎯 EXEMPLOS PRÁTICOS

### Cenário 1: Terminal acabou de abrir
```powershell
# Ir para Python4Work e rodar
cd Desktop\Python4Work\python4Work
python main.py
```

### Cenário 2: Quero rodar o NoLog
```powershell
# Ir para NoLog e rodar
cd Desktop\Python4Work\Nolog
python nolog_gui.py
```

### Cenário 3: Estou em alguma pasta aleatória
```powershell
# Usar caminho completo
python "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work\main.py"
```

### Cenário 4: Rodar e voltar para onde estava
```powershell
# Para Python4Work
Push-Location "c:\Users\giuseppe_oliveira\Desktop\Python4Work\python4Work"
python main.py
Pop-Location

# Para NoLog
Push-Location "c:\Users\giuseppe_oliveira\Desktop\Python4Work\Nolog"
python nolog_gui.py
Pop-Location
```
