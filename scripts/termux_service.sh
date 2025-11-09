 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/scripts/termux_service.sh b/scripts/termux_service.sh
new file mode 100755
index 0000000000000000000000000000000000000000..75caa74087dab22374ff482b4b0453ed38793141
--- /dev/null
+++ b/scripts/termux_service.sh
@@ -0,0 +1,14 @@
+#!/data/data/com.termux/files/usr/bin/bash
+set -euo pipefail
+
+SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
+cd "$PROJECT_ROOT"
+
+termux-wake-lock || true
+
+export JARWIS_INPUT_BACKEND="${JARWIS_INPUT_BACKEND:-termux}"
+export JARWIS_PASSIVE_SECONDS="${JARWIS_PASSIVE_SECONDS:-4.0}"
+export JARWIS_COMMAND_SECONDS="${JARWIS_COMMAND_SECONDS:-6.0}"
+
+python main.py "$@"
 
EOF
)
