"""Smoke test script for local repo sanity checks.

This script performs lightweight import checks and simple instantiation of
core components without starting any GUI mainloops. Run locally to verify
basic refactor integrity.
"""

import sys
import os

# Ensure repo root is on sys.path for imports when script is run from scripts/
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, repo_root)

if __name__ == "__main__":
    print("Running smoke checks...")
    ok = True

    try:
        import interfaces.interface_profissional as iface
        print("OK: imported interfaces.interface_profissional")
    except Exception as e:
        print("ERROR importing interfaces.interface_profissional:", e)
        ok = False

    try:
        from src.nologout import NoLogoutCore
        n = NoLogoutCore()
        status = n.get_status()
        print("OK: NoLogoutCore instantiated, status keys:", list(status.keys()))
    except Exception as e:
        print("ERROR with NoLogoutCore:", e)
        ok = False

    try:
        from core.theme_manager import ThemeManager
        tm = ThemeManager()
        print("OK: ThemeManager default:", tm.get_theme()['name'])
    except Exception as e:
        print("ERROR with ThemeManager:", e)
        ok = False

    if ok:
        print("SMOKE TESTS PASSED")
        sys.exit(0)
    else:
        print("SMOKE TESTS FAILED")
        sys.exit(2)
