# NoLog - Prevenção de Logout Automático

## 📋 Descrição

Aplicação simples para prevenir logout automático por inatividade no Windows, mantendo a sessão ativa e a VPN conectada.

## 🎯 Funcionalidades

- ✅ Simula movimento de mouse periodicamente (1 pixel - imperceptível)
- ✅ Simula pressionamento de tecla Shift (não imprime nada)
- ✅ Previne suspensão do sistema
- ✅ Interface gráfica simples e intuitiva
- ✅ **Funciona SEM privilégios de administrador**
- ✅ Controle visual claro de início/parada
- ✅ Contador de ações em tempo real
- ✅ **Sons de notificação** ao iniciar e parar (pode ser desativado)
- ✅ Checkbox para ativar/desativar sons pela interface

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **pyautogui**: Simulação de entrada de mouse e teclado
- **tkinter**: Interface gráfica nativa do Windows
- **ctypes**: Controle de configurações do Windows (opcional)

## 📦 Instalação

```bash
cd Nolog
pip install -r requirements.txt
```

## 🚀 Como Usar

### Modo GUI (Interface Gráfica) - Recomendado

**Opção 1 - Duplo clique no arquivo:**
- Clique duas vezes em `INICIAR.bat`

**Opção 2 - Linha de comando:**
```bash
cd Nolog
python nolog_gui.py
```

### Modo CLI (Linha de Comando)
```bash
cd Nolog
python nolog_cli.py
```

Para parar, pressione `Ctrl+C`

## 🎨 Interface

A aplicação possui uma interface **simples, clara e intuitiva**:

- **Janela Redimensionável**: Você pode ajustar o tamanho da janela como preferir
- **Indicador Visual Grande**: Círculo vermelho = Parado | Verde = Ativo
- **Contador de Ações**: Mostra quantas vezes agiu
- **Botão Único Inteligente**: 
  - **Verde** "▶ INICIAR PROTEÇÃO" quando parado - Clique para iniciar
  - **Vermelho** "■ PARAR PROTEÇÃO" quando ativo - Clique para parar
  - O botão muda automaticamente conforme o estado!
- **Informações Organizadas**: Intervalo e última ação sempre visíveis

### Como o Botão Funciona

O aplicativo tem **UM ÚNICO BOTÃO** que muda de acordo com o estado:

1. **Estado Inicial**: Botão VERDE "▶ INICIAR PROTEÇÃO"
   - Clique para iniciar a proteção
   
2. **Proteção Ativa**: Botão muda para VERMELHO "■ PARAR PROTEÇÃO"
   - Clique para parar a proteção
   
3. **Volta ao Início**: Botão volta a ficar VERDE

**Simples assim: Um botão, duas funções, sem confusão!**

## ⚙️ Configuração

Edite o arquivo `config.json` para ajustar:
- `interval_seconds`: Intervalo entre ações (padrão: 60 segundos)
- `mouse_movement`: true/false - Ativar movimento de mouse
- `key_press`: true/false - Ativar pressionamento de teclas
- `prevent_sleep`: true/false - Prevenir modo de suspensão
- `movement_distance`: Distância do movimento do mouse em pixels
- `sound_enabled`: true/false - Ativar sons de notificação

**Exemplo de uso**:
- Para testes rápidos: `"interval_seconds": 10`
- Para uso normal: `"interval_seconds": 60` ou `120`

### 🔊 Sons de Notificação

A aplicação emite sons quando você inicia ou para a proteção:
- **Iniciar**: Dois bips ascendentes (800Hz → 1000Hz) 🎵
- **Parar**: Um bip descendente (600Hz) 🎵

Para desativar os sons:
- Use o checkbox "🔊 Sons de notificação" na interface
- Ou edite `config.json` e mude `"sound_enabled": false`

## ✅ Funcionamento sem Administrador

Esta aplicação foi desenvolvida para funcionar **sem privilégios de administrador**:

- Usa APIs do Windows disponíveis para usuários normais
- Se alguma funcionalidade exigir admin, ela é ignorada silenciosamente
- A aplicação continua funcionando normalmente

## 🔒 Segurança e Boas Práticas

Esta ferramenta é destinada para uso pessoal e profissional legítimo:

✅ **USE PARA**:
- Manter sua sessão ativa durante trabalho legítimo
- Evitar desconexão da VPN durante pausas curtas
- Prevenir perda de trabalho por logout automático

❌ **NÃO USE PARA**:
- Burlar políticas de segurança corporativas obrigatórias
- Falsificar horas de trabalho ou presença
- Violar termos de uso de sistemas corporativos

## ⚠️ Notas Importantes

- A aplicação NÃO desabilita políticas de segurança corporativas
- Use responsavelmente e de acordo com as políticas da sua empresa
- Funciona em contas sem privilégios de administrador
- O movimento do mouse é mínimo (1 pixel) e imperceptível
- A tecla Shift não interfere em nenhuma aplicação

## 🛑 Como Parar

**3 formas de parar a aplicação**:
1. Clique no botão **"■ PARAR"**
2. Feche a janela (vai confirmar se está ativo)
3. Mova o mouse para o canto superior esquerdo (failsafe do pyautogui)

## 📝 Licença

Uso pessoal e educacional.
