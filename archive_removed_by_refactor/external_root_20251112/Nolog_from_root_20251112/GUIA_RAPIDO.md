# 🚀 GUIA RÁPIDO - NoLog

## Como Usar (Passo a Passo)

### 1️⃣ INICIAR A APLICAÇÃO
- Dê **duplo clique** em `INICIAR.bat`
- OU execute: `python nolog_gui.py`

### 2️⃣ USAR O BOTÃO ÚNICO
**O botão muda automaticamente:**

- **Quando PARADO**: Botão VERDE "▶ INICIAR PROTEÇÃO"
  - Clique para iniciar a proteção
  - 🎵 Ouvirá dois bips ascendentes (se o som estiver ativo)
  - Botão muda para VERMELHO

- **Quando ATIVO**: Botão VERMELHO "■ PARAR PROTEÇÃO"
  - Clique para parar a proteção
  - 🎵 Ouvirá um bip (se o som estiver ativo)
  - Botão volta a ficar VERDE

**É só um clique! O botão faz tudo!**

### 3️⃣ ATIVAR/DESATIVAR SONS
- Marque/desmarque o checkbox **"🔊 Sons de notificação"**
- Quando marcado, você ouvirá sons ao iniciar/parar
- Quando desmarcado, a aplicação fica silenciosa

## 🎨 Interface

```
┌────────────────────────────────────┐
│        🛡️ NoLog                    │
│   Mantenha sua sessão ativa        │
├────────────────────────────────────┤
│                                    │
│    ⭕ PARADO / ATIVO               │
│    Status da proteção              │
│                                    │
├────────────────────────────────────┤
│                                    │
│            0                       │
│      AÇÕES REALIZADAS              │
│      ─────────────                 │
│      Intervalo: 10 segundos        │
│      Última ação: Nenhuma          │
│                                    │
├────────────────────────────────────┤
│                                    │
│   ╔══════════════════════════╗    │
│   ║                          ║    │
│   ║  ▶  INICIAR PROTEÇÃO    ║    │  ← BOTÃO ÚNICO
│   ║                          ║    │    Verde = Inicia
│   ╚══════════════════════════╝    │    Vermelho = Para
│                                    │
│   Clique no botão para             │
│   Iniciar ou Parar                 │
│                                    │
└────────────────────────────────────┘
```

## 💡 Funcionamento do Botão

**VERDE (▶ INICIAR PROTEÇÃO)**
- Clique para INICIAR
- Botão fica VERMELHO
- Status: ATIVO (verde)
- Contador começa a subir

**VERMELHO (■ PARAR PROTEÇÃO)**  
- Clique para PARAR
- Botão volta a ficar VERDE
- Status: PARADO (vermelho)
- Proteção desligada

## ⚙️ Configurar Intervalo

Edite `config.json`:
- Para teste: `"interval_seconds": 10`
- Para uso normal: `"interval_seconds": 60` ou `120`

## 🛑 Formas de Parar

1. ✅ Clique no botão (quando estiver VERMELHO)
2. ✅ Feche a janela (X no canto) - ele vai confirmar
3. ✅ Mova o mouse para o canto superior esquerdo (failsafe)
