#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "$PROJECT_ROOT"

termux-wake-lock || true

export JARWIS_INPUT_BACKEND="${JARWIS_INPUT_BACKEND:-termux}"
export JARWIS_PASSIVE_SECONDS="${JARWIS_PASSIVE_SECONDS:-4.0}"
export JARWIS_COMMAND_SECONDS="${JARWIS_COMMAND_SECONDS:-6.0}"

python main.py "$@"
