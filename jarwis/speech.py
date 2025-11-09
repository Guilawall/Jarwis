 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/jarwis/speech.py b/jarwis/speech.py
new file mode 100644
index 0000000000000000000000000000000000000000..801a1c9b1fefbd4de3ec209fb782e8bd8b7d2a05
--- /dev/null
+++ b/jarwis/speech.py
@@ -0,0 +1,99 @@
+"""Entrada de áudio e síntese de voz."""
+from __future__ import annotations
+
+import tempfile
+from pathlib import Path
+
+import speech_recognition as sr
+
+from .config import AssistantConfig
+from .termux import TermuxCommandError, command_available, record_microphone, speak
+
+
+class SpeechError(RuntimeError):
+    """Erro crítico na captura ou síntese de voz."""
+
+
+class SpeechEngine:
+    """Cuida da captura de áudio e da fala do Jarwis."""
+
+    def __init__(self, config: AssistantConfig) -> None:
+        self._config = config
+        self._recognizer = sr.Recognizer()
+        self._recognizer.pause_threshold = 0.8
+        self._recognizer.dynamic_energy_threshold = True
+        self._backend = self._resolve_backend(config.input_backend)
+
+    def _resolve_backend(self, requested: str) -> str:
+        requested = (requested or "auto").lower()
+        if requested not in {"auto", "termux", "microphone"}:
+            raise SpeechError(f"Backend de áudio desconhecido: {requested}")
+        if requested == "termux":
+            if not command_available(self._config.termux_microphone_command):
+                raise SpeechError(
+                    "termux-microphone-record não está disponível. Instale o Termux:API."
+                )
+            return "termux"
+        if requested == "microphone":
+            return "microphone"
+        if command_available(self._config.termux_microphone_command):
+            return "termux"
+        return "microphone"
+
+    def listen(self, duration: float) -> str:
+        """Captura uma frase e retorna o texto reconhecido."""
+
+        if self._backend == "termux":
+            return self._listen_with_termux(duration)
+        return self._listen_with_microphone(duration)
+
+    def speak(self, text: str) -> None:
+        """Reproduz uma resposta falada (ou faz fallback para o console)."""
+
+        try:
+            speak(self._config.termux_tts_command, text)
+        except TermuxCommandError:
+            print(f"Jarwis: {text}")
+
+    def _listen_with_termux(self, duration: float) -> str:
+        destination = Path(tempfile.gettempdir()) / "jarwis-capture.wav"
+        try:
+            record_microphone(
+                self._config.termux_microphone_command,
+                destination,
+                max(duration, 1.0),
+                self._config.sample_rate,
+            )
+        except TermuxCommandError as exc:
+            raise SpeechError(str(exc)) from exc
+        try:
+            with sr.AudioFile(str(destination)) as source:
+                audio = self._recognizer.record(source)
+        finally:
+            if destination.exists():
+                destination.unlink()
+        return self._recognize(audio)
+
+    def _listen_with_microphone(self, duration: float) -> str:
+        try:
+            microphone = sr.Microphone(sample_rate=self._config.sample_rate)
+        except Exception as exc:  # pragma: no cover - depende do SO
+            raise SpeechError(
+                "Não há microfone disponível. Instale o PyAudio ou use o backend Termux."
+            ) from exc
+        with microphone as source:
+            self._recognizer.adjust_for_ambient_noise(source, duration=0.3)
+            audio = self._recognizer.listen(source, phrase_time_limit=duration)
+        return self._recognize(audio)
+
+    def _recognize(self, audio: sr.AudioData) -> str:
+        try:
+            text = self._recognizer.recognize_google(audio, language=self._config.language)
+        except sr.UnknownValueError:
+            return ""
+        except sr.RequestError as exc:  # pragma: no cover - depende de rede externa
+            raise SpeechError(f"Falha na transcrição: {exc}") from exc
+        return text.strip()
+
+
+__all__ = ["SpeechEngine", "SpeechError"]
 
EOF
)
