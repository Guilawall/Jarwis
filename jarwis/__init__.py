 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/jarwis/__init__.py b/jarwis/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..186cfe0b45ff9ccce4ddc8a315d72696691a129d
--- /dev/null
+++ b/jarwis/__init__.py
@@ -0,0 +1,6 @@
+"""Núcleo do assistente Jarwis."""
+
+from .assistant import JarwisAssistant
+from .config import AssistantConfig
+
+__all__ = ["JarwisAssistant", "AssistantConfig"]
 
EOF
)
