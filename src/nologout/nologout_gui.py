"""Shim GUI: `src.nologout` aponta para `src.manter_sessao` GUI.

Este arquivo atua como wrapper para compatibilidade e re-exporta a
implementação em `manter_sessao`. Mantê-lo evita a presença de duas
implementações idênticas no repositório.
"""
from ..manter_sessao import ManterSessaoGUI as NoLogoutGUI

__all__ = ["NoLogoutGUI"]
