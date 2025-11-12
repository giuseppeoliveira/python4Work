"""
Compatibilidade legada para o pacote `src.nologout`.

Este arquivo expõe aliases para as novas implementações em
`src.manter_sessao` por compatibilidade com código que ainda importe
o pacote antigo. A intenção é manter um shim até que todas as
referências sejam migradas para `manter_sessao`.
"""
from ..manter_sessao import ManterSessaoCore, ManterSessaoGUI

# Compatibilidade (aliases) — evitar o uso direto, migrar para manter_sessao
NoLogoutCore = ManterSessaoCore
NoLogoutGUI = ManterSessaoGUI

__all__ = ['NoLogoutCore', 'NoLogoutGUI']
