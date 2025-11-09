 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/main.py b/main.py
new file mode 100644
index 0000000000000000000000000000000000000000..8e681eb85bd5fa25e840ee4d0ad80cb0217cc737
--- /dev/null
+++ b/main.py
@@ -0,0 +1,70 @@
+"""Entrada principal do assistente Jarwis."""
+from __future__ import annotations
+
+import argparse
+import logging
+import sys
+
+from jarwis import JarwisAssistant
+from jarwis.config import load_config_from_env
+
+
+def build_parser() -> argparse.ArgumentParser:
+    parser = argparse.ArgumentParser(description="Assistente Jarwis em modo escuta")
+    parser.add_argument("--wake-word", help="Palavra de ativação", default=None)
+    parser.add_argument(
+        "--input-backend",
+        choices=["auto", "termux", "microphone"],
+        default=None,
+        help="Origem do áudio (auto detecta, Termux ou microfone padrão)",
+    )
+    parser.add_argument(
+        "--passive-seconds", type=float, default=None, help="Tempo para ouvir o chamado"
+    )
+    parser.add_argument(
+        "--command-seconds", type=float, default=None, help="Tempo máximo para o comando"
+    )
+    parser.add_argument(
+        "--language", default=None, help="Idioma usado na transcrição (ex: pt-BR)"
+    )
+    parser.add_argument(
+        "--once",
+        action="store_true",
+        help="Escuta apenas uma vez depois do wake word e finaliza",
+    )
+    parser.add_argument(
+        "--log-level",
+        default="WARNING",
+        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
+        help="Nível de log emitido no console",
+    )
+    return parser
+
+
+def configure_logging(level: str) -> None:
+    logging.basicConfig(
+        level=getattr(logging, level.upper(), logging.INFO),
+        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
+    )
+
+
+def main(argv: list[str] | None = None) -> int:
+    parser = build_parser()
+    args = parser.parse_args(argv)
+    configure_logging(args.log_level)
+
+    config = load_config_from_env(
+        wake_word=args.wake_word,
+        input_backend=args.input_backend,
+        passive_listen_seconds=args.passive_seconds,
+        command_listen_seconds=args.command_seconds,
+        language=args.language,
+    )
+
+    assistant = JarwisAssistant(config)
+    assistant.run(loop_once=args.once)
+    return 0
+
+
+if __name__ == "__main__":  # pragma: no cover - execução direta
+    sys.exit(main())
 
EOF
)
