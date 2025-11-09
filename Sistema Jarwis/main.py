"""Wrapper para executar o main real quando o usuário está nesta pasta.

Este arquivo só encaminha a execução para `../main.py`, permitindo que comandos
executados dentro da pasta `Sistema Jarwis` funcionem igual ao diretório raiz.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "main.py"

if not TARGET.exists():
    raise FileNotFoundError(
        "Não foi possível localizar main.py no diretório pai. Volte para o "
        "repositório original com 'cd ..' e tente novamente."
    )

sys.path.insert(0, str(ROOT))
runpy.run_path(str(TARGET), run_name="__main__"
