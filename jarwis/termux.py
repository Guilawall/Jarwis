 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/jarwis/termux.py b/jarwis/termux.py
new file mode 100644
index 0000000000000000000000000000000000000000..422bc1c2c789a6c932bfa523da09694dc941beb8
--- /dev/null
+++ b/jarwis/termux.py
@@ -0,0 +1,109 @@
+"""Integrações com Termux:API."""
+from __future__ import annotations
+
+import json
+import shutil
+import subprocess
+from pathlib import Path
+from typing import Iterable, List
+
+
+class TermuxCommandError(RuntimeError):
+    """Erro ao executar um comando Termux."""
+
+    def __init__(self, command: Iterable[str], stderr: str) -> None:
+        self.command = list(command)
+        message = f"Falha ao executar {' '.join(self.command)}: {stderr.strip()}"
+        super().__init__(message)
+        self.stderr = stderr
+
+
+def command_available(command: str) -> bool:
+    """Verifica se um comando Termux está disponível na PATH."""
+
+    return shutil.which(command) is not None
+
+
+def speak(tts_command: str, text: str) -> None:
+    """Fala uma frase usando termux-tts-speak."""
+
+    if not command_available(tts_command):
+        raise TermuxCommandError([tts_command], "Comando Termux TTS indisponível")
+    result = subprocess.run([tts_command, text], capture_output=True, text=True)
+    if result.returncode != 0:
+        raise TermuxCommandError([tts_command, text], result.stderr)
+
+
+def record_microphone(
+    command: str,
+    destination: Path,
+    duration: float,
+    sample_rate: int,
+) -> None:
+    """Grava áudio para ``destination`` usando termux-microphone-record."""
+
+    if not command_available(command):
+        raise TermuxCommandError([command], "termux-microphone-record não encontrado")
+
+    attempts: List[List[str]] = []
+    for flag in ("-l", "-d", "-e"):
+        attempts.append(
+            [
+                command,
+                "-f",
+                str(destination),
+                flag,
+                f"{duration:.2f}",
+                "-r",
+                str(sample_rate),
+            ]
+        )
+    attempts.append([command, "-f", str(destination), "-r", str(sample_rate)])
+
+    last_error = ""
+    for args in attempts:
+        try:
+            result = subprocess.run(args, capture_output=True, text=True)
+        except FileNotFoundError as exc:  # pragma: no cover - depende do ambiente
+            raise TermuxCommandError(args, str(exc)) from exc
+        if result.returncode == 0:
+            return
+        last_error = result.stderr
+    raise TermuxCommandError(attempts[-1], last_error or "falha ao gravar áudio")
+
+
+def list_contacts(command: str) -> list[dict[str, object]]:
+    """Obtém os contatos disponíveis via termux-contact-list."""
+
+    if not command_available(command):
+        raise TermuxCommandError([command], "termux-contact-list não encontrado")
+    result = subprocess.run([command], capture_output=True, text=True)
+    if result.returncode != 0:
+        raise TermuxCommandError([command], result.stderr)
+    try:
+        data = json.loads(result.stdout or "[]")
+    except json.JSONDecodeError as exc:  # pragma: no cover - depende do Termux
+        raise TermuxCommandError([command], f"JSON inválido: {exc}") from exc
+    if not isinstance(data, list):
+        return []
+    return [item for item in data if isinstance(item, dict)]
+
+
+def start_phone_call(command: str, number: str) -> None:
+    """Inicia uma chamada telefônica usando termux-telephony-call."""
+
+    if not command_available(command):
+        raise TermuxCommandError([command, number], "termux-telephony-call não encontrado")
+    result = subprocess.run([command, number], capture_output=True, text=True)
+    if result.returncode != 0:
+        raise TermuxCommandError([command, number], result.stderr)
+
+
+__all__ = [
+    "TermuxCommandError",
+    "command_available",
+    "speak",
+    "record_microphone",
+    "list_contacts",
+    "start_phone_call",
+]
 
EOF
)
