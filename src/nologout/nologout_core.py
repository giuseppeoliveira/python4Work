"""Shim de compatibilidade: `src.nologout` agora aponta para `src.manter_sessao`.

Este arquivo permanece para evitar que imports legados quebrem. Ele re-exporta
o nome antigo como alias para a nova implementação em `manter_sessao`.
"""
from ..manter_sessao import ManterSessaoCore as NoLogoutCore

__all__ = ["NoLogoutCore"]
