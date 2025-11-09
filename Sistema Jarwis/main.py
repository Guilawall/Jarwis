 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/Sistema Jarwis/main.py b/Sistema Jarwis/main.py
new file mode 100644
index 0000000000000000000000000000000000000000..0d4703b3f5c49283e2910a2e2c0f955fb7dcf0ec
--- /dev/null
+++ b/Sistema Jarwis/main.py	
@@ -0,0 +1,22 @@
+"""Wrapper para executar o main real quando o usuário está nesta pasta.
+
+Este arquivo só encaminha a execução para `../main.py`, permitindo que comandos
+executados dentro da pasta `Sistema Jarwis` funcionem igual ao diretório raiz.
+"""
+from __future__ import annotations
+
+import runpy
+import sys
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parents[1]
+TARGET = ROOT / "main.py"
+
+if not TARGET.exists():
+    raise FileNotFoundError(
+        "Não foi possível localizar main.py no diretório pai. Volte para o "
+        "repositório original com 'cd ..' e tente novamente."
+    )
+
+sys.path.insert(0, str(ROOT))
+runpy.run_path(str(TARGET), run_name="__main__")
 
EOF
)
