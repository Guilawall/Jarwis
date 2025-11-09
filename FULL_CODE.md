diff --git a/FULL_CODE.md b/FULL_CODE.md
new file mode 100644
index 0000000000000000000000000000000000000000..f2f538ab227784c6bf841c8b1f7f7eb78b4d9dd2
--- /dev/null
+++ b/FULL_CODE.md
@@ -0,0 +1,1111 @@
+# Código completo do Jarwis
+
+Este arquivo reúne todos os arquivos principais do projeto para que você possa copiar e colar diretamente no GitHub. Cada seção abaixo mostra o caminho do arquivo e o conteúdo exato que deve ser colado.
+
+## `.gitignore`
+```gitignore
+__pycache__/
+*.pyc
+```
+
+## `README.md`
+```markdown
+# Assistente Jarwis reescrito
+
+Este projeto implementa um protótipo do "Jarwis": um assistente de voz em português
+que fica escutando em segundo plano, responde quando ouve o chamado "Jarwis" e
+executa ações específicas:
+
+- Responde "Senhor, o que deseja?" após ouvir o wake word.
+- Realiza chamadas telefônicas para contatos salvos quando você diz
+  **"Jarwis… ligar para (nome do contato)"**.
+- Mantém uma lista persistente: é possível adicionar, remover, consultar todos os
+  itens ou perguntar qual é o *n*-ésimo termo cadastrado.
+
+O foco principal é o Android via Termux + Termux:API, mas o código também pode ser
+executado em um computador com microfone.
+
+## Comandos suportados
+
+Depois do wake word, o Jarwis entende as frases abaixo (maiúsculas apenas para
+ilustração):
+
+| Frase | Ação |
+| ----- | ---- |
+| `Jarwis… ligar para Maria` | Procura "Maria" nos contatos e inicia uma chamada telefônica. |
+| `Jarwis… adicionar café à lista` | Armazena a palavra "café" na lista persistente. |
+| `Jarwis… retirar café da lista` | Remove "café" se existir, ou responde "Senhor, isso não tem na lista." |
+| `Jarwis… o que tem na lista?` | Lê em voz alta todos os itens cadastrados. |
+| `Jarwis… qual é o quinto termo da lista?` | Informa o item na posição solicitada (ordinais até vigésimo ou números). |
+
+A lista fica salva em `~/.jarwis/lista.json`, permitindo que o conteúdo seja
+mantido entre execuções.
+
+## Instalação no Android (Termux)
+
+1. Instale [Termux](https://f-droid.org/packages/com.termux/) e o complemento
+   [Termux:API](https://f-droid.org/packages/com.termux.api/).
+2. Abra o Termux, conceda acesso ao armazenamento e prepare os pacotes básicos:
+   ```bash
+   termux-setup-storage
+   pkg update
+   pkg install python clang fftw libffi ffmpeg termux-api git
+   python -m pip install --upgrade pip
+   ```
+3. Clone este repositório (substitua pelo endereço correto se estiver usando um fork):
+   ```bash
+   git clone https://github.com/Guilawall/Jarwis.git
+   cd Jarwis
+   ```
+
+  > **Baixou um ZIP pelo celular?** O Android costuma descompactar em uma
+  > pasta com espaço, como `Sistema Jarwis`. Nesse caso:
+  >
+  > 1. Rode `ls` dentro da pasta recém-criada. Se o comando listar apenas
+  >    `Sistema Jarwis`, significa que você ainda está um nível acima do
+  >    projeto original.
+  > 2. Entre nessa pasta com aspas: `cd "Sistema Jarwis"` e rode `ls` de
+  >    novo. Este repositório agora traz um **atalho** lá dentro: um novo
+  >    `README.md`, um `main.py` que aponta para o original e arquivos
+  >    `requirements*.txt` que importam os do diretório pai.
+  > 3. Mesmo assim, a recomendação é voltar para o diretório raiz usando
+  >    `cd ..` ou renomear a pasta para evitar o espaço: `mv "Sistema Jarwis" Jarwis`
+  >    e voltar para ela com `cd Jarwis` antes de continuar.
+
+   Confirme que você está dentro da pasta correta e que os arquivos
+   `main.py` e `requirements.txt` aparecem na listagem. Esses nomes são
+   **exatamente** assim, com `requirements` no plural e a extensão `.txt`.
+
+   ```bash
+   pwd               # deve terminar com .../Jarwis
+   ls                # precisa mostrar main.py e requirements.txt
+   cat requirements.txt
+   ```
+
+   O arquivo `requirements.txt` precisa conter **apenas** a linha abaixo. Se aparecer
+   qualquer outra coisa (por exemplo, um comando começando com `git`), recrie o
+   arquivo com o comando mostrado em seguida antes de instalar as dependências.
+
+   ```text
+   SpeechRecognition>=3.10
+   ```
+
+   ```bash
+   printf 'SpeechRecognition>=3.10\n' > requirements.txt
+   pip install -r requirements.txt
+   ```
+4. Execute o assistente indicando o backend Termux. A primeira execução pedirá
+   permissão de microfone no Android. Use `./main.py` para garantir que o Python
+   procure o arquivo dentro da pasta atual:
+   ```bash
+   python ./main.py --input-backend termux --log-level INFO
+   ```
+
+O Jarwis criará o diretório `~/.jarwis/` para armazenar a lista e arquivos
+temporários de áudio.
+
+### Rodando automaticamente ao iniciar o Termux
+
+O script `scripts/termux_service.sh` aplica `termux-wake-lock` e inicia o Jarwis
+com o backend Termux. Para utilizá-lo com o aplicativo Termux:Boot:
+
+```bash
+mkdir -p ~/.termux/boot
+cp scripts/termux_service.sh ~/.termux/boot/jarwis.sh
+chmod +x ~/.termux/boot/jarwis.sh
+```
+
+Opcionalmente configure variáveis de ambiente antes de chamar o script para ajustar
+wake word ou tempos de escuta (veja a seção "Configuração").
+
+## Execução em computadores
+
+Em sistemas Linux/macOS/Windows com microfone compatível com PyAudio:
+
+```bash
+python -m venv .venv
+source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
+pip install -r requirements-desktop.txt
+python ./main.py --input-backend microphone
+```
+
+Se o PyAudio não estiver disponível, utilize o backend Termux.
+
+## Configuração
+
+As opções podem ser fornecidas pela linha de comando ou por variáveis de ambiente.
+Se um parâmetro não for informado, o Jarwis usa os seguintes valores padrão:
+
+| Variável / Flag | Padrão | Descrição |
+| --------------- | ------ | --------- |
+| `--wake-word` / `JARWIS_WAKE_WORD` | `jarwis` | Palavra de ativação (aceita variações como "jarvis"). |
+| `--input-backend` / `JARWIS_INPUT_BACKEND` | `auto` | `termux`, `microphone` ou `auto` (prioriza Termux). |
+| `--passive-seconds` / `JARWIS_PASSIVE_SECONDS` | `4.0` | Tempo para ouvir o wake word. |
+| `--command-seconds` / `JARWIS_COMMAND_SECONDS` | `6.0` | Janela para entender o comando após o wake word. |
+| `--language` / `JARWIS_LANGUAGE` | `pt-BR` | Idioma usado pelo serviço de transcrição. |
+| `JARWIS_TERMUX_MIC` | `termux-microphone-record` | Comando utilizado para gravar áudio no Termux. |
+| `JARWIS_TERMUX_TTS` | `termux-tts-speak` | Comando de síntese de voz. |
+| `JARWIS_TERMUX_CONTACTS` | `termux-contact-list` | Comando usado para ler os contatos. |
+| `JARWIS_TERMUX_CALL` | `termux-telephony-call` | Comando usado para iniciar chamadas telefônicas. |
+
+## Dependências
+
+- `SpeechRecognition>=3.10` – transcrição de áudio via Google Speech.
+- `pyaudio` (apenas em desktops) – necessário para capturar áudio em tempo real.
+
+No Termux, todas as interações com o microfone, contatos, TTS e telefone passam
+pelos binários do Termux:API.
+
+## Dicas de uso
+
+- A transcrição depende da internet (serviço Google). Para respostas mais rápidas,
+  tente falar frases completas logo após ouvir "Senhor, o que deseja?".
+- O comando de chamadas procura aproximações por nome. Se houver ambiguidade,
+  renomeie os contatos para evitar confusões.
+- Para limpar a lista manualmente, apague o arquivo `~/.jarwis/lista.json`.
+
+Divirta-se com o seu novo Jarwis!
+```
+
+## `requirements.txt`
+```text
+SpeechRecognition>=3.10
+```
+
+## `requirements-desktop.txt`
+```text
+SpeechRecognition>=3.10
+PyAudio>=0.2.13
+```
+
+## `main.py`
+```python
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
+```
+
+## `jarwis/__init__.py`
+```python
+"""Núcleo do assistente Jarwis."""
+
+from .assistant import JarwisAssistant
+from .config import AssistantConfig
+
+__all__ = ["JarwisAssistant", "AssistantConfig"]
+```
+
+## `jarwis/assistant.py`
+```python
+"""Orquestração principal do Jarwis."""
+from __future__ import annotations
+
+import logging
+from typing import Optional
+
+from .commands import ParsedCommand, parse_command
+from .config import AssistantConfig
+from .contacts import ContactBook
+from .memory import MemoryList
+from .speech import SpeechEngine, SpeechError
+
+logger = logging.getLogger(__name__)
+
+
+class JarwisAssistant:
+    """Assistente de voz que reage ao chamado "Jarwis"."""
+
+    def __init__(self, config: Optional[AssistantConfig] = None) -> None:
+        self.config = config or AssistantConfig()
+        self.speech = SpeechEngine(self.config)
+        self.memory = MemoryList(self.config.memory_file)
+        self.contacts = ContactBook(self.config)
+
+    def run(self, loop_once: bool = False) -> None:
+        """Inicia o laço principal de escuta."""
+
+        logger.info("Assistente iniciado com wake words: %s", ", ".join(self.config.wake_words))
+        try:
+            while True:
+                heard = self.speech.listen(self.config.passive_listen_seconds)
+                if not heard:
+                    if loop_once:
+                        break
+                    continue
+                logger.debug("Transcrição passiva: %s", heard)
+                if not self._is_wake_word_present(heard):
+                    if loop_once:
+                        break
+                    continue
+                self.speech.speak("Senhor, o que deseja?")
+                command_text = self.speech.listen(self.config.command_listen_seconds)
+                if not command_text:
+                    self.speech.speak("Não ouvi nenhum pedido, senhor.")
+                    if loop_once:
+                        break
+                    continue
+                logger.info("Comando reconhecido: %s", command_text)
+                response = self._handle_command(command_text)
+                if response:
+                    self.speech.speak(response)
+                if loop_once:
+                    break
+        except KeyboardInterrupt:
+            logger.info("Jarwis interrompido pelo usuário.")
+        except SpeechError as exc:
+            logger.error("Erro de áudio: %s", exc)
+            raise
+
+    def _is_wake_word_present(self, text: str) -> bool:
+        lowered = text.lower()
+        return any(word in lowered for word in self.config.wake_words)
+
+    def _handle_command(self, command_text: str) -> str:
+        parsed = parse_command(command_text)
+        if parsed is None:
+            return "Ainda não sei como fazer isso, senhor."
+        if parsed.action == "call":
+            return self._handle_call(parsed)
+        if parsed.action == "add" and parsed.text:
+            self.memory.add(parsed.text)
+            return f"Adicionei {parsed.text} à lista, senhor."
+        if parsed.action == "list_all":
+            items = self.memory.items()
+            if not items:
+                return "A lista está vazia, senhor."
+            itens_formatados = ", ".join(items)
+            return f"Na lista estão: {itens_formatados}."
+        if parsed.action == "nth" and parsed.index:
+            item = self.memory.nth(parsed.index)
+            if item is None:
+                return "Ainda não tenho tantos itens assim na lista, senhor."
+            return f"O {parsed.index}º termo da lista é {item}."
+        if parsed.action == "remove" and parsed.text:
+            removed = self.memory.remove(parsed.text)
+            if not removed:
+                return "Senhor, isso não tem na lista."
+            return f"Retirei {parsed.text} da lista, senhor."
+        return "Ainda não sei como fazer isso, senhor."
+
+    def _handle_call(self, parsed: ParsedCommand) -> str:
+        if not parsed.text:
+            return "Preciso saber para quem ligar, senhor."
+        contact = self.contacts.find(parsed.text)
+        if contact is None:
+            return f"Não encontrei {parsed.text} nos contatos, senhor."
+        if not self.contacts.call(contact):
+            return "Não consegui iniciar a chamada, senhor."
+        return f"Ligando para {contact.name}."
+
+
+__all__ = ["JarwisAssistant"]
+```
+
+## `jarwis/commands.py`
+```python
+"""Analisador dos comandos de voz do Jarwis."""
+from __future__ import annotations
+
+import re
+import unicodedata
+from dataclasses import dataclass
+from typing import Optional
+
+
+@dataclass
+class ParsedCommand:
+    action: str
+    text: str | None = None
+    index: int | None = None
+
+
+def parse_command(command: str) -> Optional[ParsedCommand]:
+    """Interpreta uma frase de comando e retorna a intenção."""
+
+    command = command.strip()
+    if not command:
+        return None
+    lowered = command.lower()
+
+    call_match = re.search(r"ligar\s+para\s+(.+)", command, flags=re.IGNORECASE)
+    if call_match:
+        name = call_match.group(1).strip().rstrip("?.!")
+        return ParsedCommand("call", text=name)
+
+    if re.search(r"o que tem na lista", lowered):
+        return ParsedCommand("list_all")
+
+    nth_match = re.search(
+        r"qual\s+(?:é|e)\s+(?:o|a)?\s*([^\?]+?)\s+termo\s+da\s+lista",
+        command,
+        flags=re.IGNORECASE,
+    )
+    if nth_match:
+        index = _parse_ordinal(nth_match.group(1))
+        if index is not None:
+            return ParsedCommand("nth", index=index)
+
+    remove_match = re.search(
+        r"retirar\s+(.+?)\s+da\s+lista",
+        command,
+        flags=re.IGNORECASE,
+    )
+    if remove_match:
+        item = remove_match.group(1).strip().rstrip("?.!")
+        return ParsedCommand("remove", text=item)
+
+    add_match = re.search(
+        r"adicionar\s+(.+?)\s+(?:na|a|à)\s+lista",
+        command,
+        flags=re.IGNORECASE,
+    )
+    if add_match:
+        item = add_match.group(1).strip().rstrip("?.!")
+        return ParsedCommand("add", text=item)
+
+    if lowered.startswith("adicionar "):
+        item = command[10:].strip().rstrip("?.!")
+        return ParsedCommand("add", text=item)
+
+    if lowered.startswith("retirar "):
+        item = command[8:].strip().rstrip("?.!")
+        return ParsedCommand("remove", text=item)
+
+    return None
+
+
+ORDINAL_SINGLE = {
+    "primeiro": 1,
+    "primeira": 1,
+    "segundo": 2,
+    "segunda": 2,
+    "terceiro": 3,
+    "terceira": 3,
+    "quarto": 4,
+    "quarta": 4,
+    "quinto": 5,
+    "quinta": 5,
+    "sexto": 6,
+    "sexta": 6,
+    "sétimo": 7,
+    "setimo": 7,
+    "sétima": 7,
+    "setima": 7,
+    "oitavo": 8,
+    "oitava": 8,
+    "nono": 9,
+    "nona": 9,
+    "décimo": 10,
+    "decimo": 10,
+    "décima": 10,
+    "decima": 10,
+}
+
+ORDINAL_COMPOSED = {
+    "décimo primeiro": 11,
+    "decimo primeiro": 11,
+    "décima primeira": 11,
+    "decima primeira": 11,
+    "décimo segundo": 12,
+    "decimo segundo": 12,
+    "décima segunda": 12,
+    "decima segunda": 12,
+    "décimo terceiro": 13,
+    "decimo terceiro": 13,
+    "décima terceira": 13,
+    "decima terceira": 13,
+    "décimo quarto": 14,
+    "decimo quarto": 14,
+    "décima quarta": 14,
+    "decima quarta": 14,
+    "décimo quinto": 15,
+    "decimo quinto": 15,
+    "décima quinta": 15,
+    "decima quinta": 15,
+    "décimo sexto": 16,
+    "decimo sexto": 16,
+    "décima sexta": 16,
+    "decima sexta": 16,
+    "décimo sétimo": 17,
+    "decimo setimo": 17,
+    "décima sétima": 17,
+    "decima setima": 17,
+    "décimo oitavo": 18,
+    "decimo oitavo": 18,
+    "décima oitava": 18,
+    "decima oitava": 18,
+    "décimo nono": 19,
+    "decimo nono": 19,
+    "décima nona": 19,
+    "decima nona": 19,
+    "vigésimo": 20,
+    "vigesimo": 20,
+    "vigésima": 20,
+    "vigesima": 20,
+}
+
+
+def _parse_ordinal(fragment: str) -> Optional[int]:
+    fragment = fragment.strip().lower()
+    digits = re.sub(r"[^0-9]", "", fragment)
+    if digits:
+        try:
+            return int(digits)
+        except ValueError:
+            return None
+    normalized = unicodedata.normalize("NFD", fragment)
+    normalized = " ".join(
+        "".join(ch for ch in part if unicodedata.category(ch) != "Mn")
+        for part in normalized.split()
+    ).strip()
+    if normalized in ORDINAL_COMPOSED:
+        return ORDINAL_COMPOSED[normalized]
+    tokens = normalized.split()
+    if len(tokens) == 1 and tokens[0] in ORDINAL_SINGLE:
+        return ORDINAL_SINGLE[tokens[0]]
+    if len(tokens) >= 2:
+        combined = " ".join(tokens[:2])
+        if combined in ORDINAL_COMPOSED:
+            return ORDINAL_COMPOSED[combined]
+    return None
+
+
+__all__ = ["ParsedCommand", "parse_command"]
+```
+
+## `jarwis/config.py`
+```python
+"""Configurações e utilidades de carregamento do assistente."""
+from __future__ import annotations
+
+import os
+from dataclasses import dataclass, field
+from pathlib import Path
+
+
+def _env_float(name: str, default: float) -> float:
+    value = os.getenv(name)
+    if value is None:
+        return default
+    try:
+        return float(value)
+    except ValueError:
+        return default
+
+
+def _env_int(name: str, default: int) -> int:
+    value = os.getenv(name)
+    if value is None:
+        return default
+    try:
+        return int(value)
+    except ValueError:
+        return default
+
+
+@dataclass
+class AssistantConfig:
+    """Parâmetros centrais do Jarwis."""
+
+    wake_word: str = "jarwis"
+    alternate_wake_words: tuple[str, ...] = ("jarvis",)
+    language: str = "pt-BR"
+    passive_listen_seconds: float = 4.0
+    command_listen_seconds: float = 6.0
+    input_backend: str = "auto"
+    sample_rate: int = 16000
+    data_dir: Path = field(default_factory=lambda: Path.home() / ".jarwis")
+    memory_file: Path = field(init=False)
+    contact_refresh_seconds: int = 900
+    termux_microphone_command: str = "termux-microphone-record"
+    termux_tts_command: str = "termux-tts-speak"
+    termux_contact_command: str = "termux-contact-list"
+    termux_call_command: str = "termux-telephony-call"
+
+    def __post_init__(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.data_dir / "lista.json"

    @property
    def wake_words(self) -> tuple[str, ...]:
        return tuple({self.wake_word.lower(), *(w.lower() for w in self.alternate_wake_words)})


def load_config_from_env(**overrides: object) -> AssistantConfig:
    """Carrega a configuração combinando variáveis de ambiente e sobrescritas."""

    config = AssistantConfig(
        wake_word=str(overrides.get("wake_word") or os.getenv("JARWIS_WAKE_WORD", "jarwis")),
        alternate_wake_words=_resolve_alternate(overrides.get("alternate_wake_words")),
        language=str(overrides.get("language") or os.getenv("JARWIS_LANGUAGE", "pt-BR")),
        passive_listen_seconds=float(
            overrides.get("passive_listen_seconds")
            or _env_float("JARWIS_PASSIVE_SECONDS", 4.0)
        ),
        command_listen_seconds=float(
            overrides.get("command_listen_seconds")
            or _env_float("JARWIS_COMMAND_SECONDS", 6.0)
        ),
        input_backend=str(overrides.get("input_backend") or os.getenv("JARWIS_INPUT_BACKEND", "auto")),
        sample_rate=int(
            overrides.get("sample_rate") or _env_int("JARWIS_SAMPLE_RATE", 16000)
        ),
        contact_refresh_seconds=int(
            overrides.get("contact_refresh_seconds")
            or _env_int("JARWIS_CONTACT_REFRESH", 900)
            
        ),
        termux_microphone_command=str(
            overrides.get("termux_microphone_command")
            or os.getenv("JARWIS_TERMUX_MIC", "termux-microphone-record")
        ),
        termux_tts_command=str(
            overrides.get("termux_tts_command")
            or os.getenv("JARWIS_TERMUX_TTS", "termux-tts-speak")
        ),
        termux_contact_command=str(
            overrides.get("termux_contact_command")
            or os.getenv("JARWIS_TERMUX_CONTACTS", "termux-contact-list")
        ),
        termux_call_command=str(
            overrides.get("termux_call_command")
            or os.getenv("JARWIS_TERMUX_CALL", "termux-telephony-call")
        ),
        )
    data_dir = overrides.get("data_dir")
    if isinstance(data_dir, Path):
        config.data_dir = data_dir
        config.data_dir.mkdir(parents=True, exist_ok=True)
        config.memory_file = config.data_dir / "lista.json"
    elif isinstance(data_dir, str):
        config.data_dir = Path(data_dir).expanduser()
        config.data_dir.mkdir(parents=True, exist_ok=True)
        config.memory_file = config.data_dir / "lista.json"
    return config


def _resolve_alternate(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(v).lower() for v in value if v)
    raw = os.getenv("JARWIS_ALT_WAKE", "jarvis")
    return tuple(part.strip().lower() for part in raw.split(",") if part.strip())


__all__ = ["AssistantConfig", "load_config_from_env"]
```

## `jarwis/contacts.py`
```python
"""Integração com a agenda do dispositivo."""
from __future__ import annotations

import difflib
import time
from dataclasses import dataclass
from typing import List, Optional

from .config import AssistantConfig
from .termux import TermuxCommandError, list_contacts, start_phone_call


@dataclass
class Contact:
    name: str
    number: str


class ContactBook:
    """Carrega e pesquisa contatos usando o Termux:API."""

    def __init__(self, config: AssistantConfig) -> None:
        self._config = config
        self._cache: List[Contact] = []
        self._cache_timestamp: float = 0.0

    def _refresh_if_needed(self) -> None:
        now = time.time()
        if self._cache and (now - self._cache_timestamp) < self._config.contact_refresh_seconds:
            return
        try:
            raw_contacts = list_contacts(self._config.termux_contact_command)
        except TermuxCommandError:
            self._cache = []
            self._cache_timestamp = now
            return
        parsed: List[Contact] = []
        for entry in raw_contacts:
            name = str(entry.get("name") or "").strip()
            if not name:
                continue
            number = _extract_number(entry)
            if number:
                parsed.append(Contact(name=name, number=number))
        self._cache = parsed
        self._cache_timestamp = now

    def find(self, query: str) -> Optional[Contact]:
        self._refresh_if_needed()
        if not self._cache:
            return None
        normalized = query.lower().strip()
        names = [contact.name.lower() for contact in self._cache]
        matches = difflib.get_close_matches(normalized, names, n=1, cutoff=0.6)
        if matches:
            target = matches[0]
            for contact in self._cache:
                if contact.name.lower() == target:
                    return contact
        for contact in self._cache:
            if normalized in contact.name.lower():
                return contact
        return None

    def call(self, contact: Contact) -> bool:
        try:
            start_phone_call(self._config.termux_call_command, contact.number)
            return True
        except TermuxCommandError:
            return False


def _extract_number(entry: dict[str, object]) -> Optional[str]:
    number = entry.get("number")
    if isinstance(number, list) and number:
        return str(number[0])
    if isinstance(number, (str, int)):
        return str(number)
    numbers = entry.get("numbers")
    if isinstance(numbers, list) and numbers:
        first = numbers[0]
        if isinstance(first, dict):
            value = first.get("number") or first.get("value")
            if value:
                return str(value)
        return str(first)
    return None


__all__ = ["Contact", "ContactBook"]
```

## `jarwis/memory.py`
```python
"""Persistência da lista solicitada pelo usuário."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List


class MemoryList:
    """Gerencia a lista personalizada do usuário."""

    def __init__(self, storage: Path) -> None:
        self._storage = storage
        self._storage.parent.mkdir(parents=True, exist_ok=True)
        self._items: List[str] = []
        self._load()

    def _load(self) -> None:
        if not self._storage.exists():
            self._items = []
            return
        try:
            data = json.loads(self._storage.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            self._items = []
            return
        if isinstance(data, list):
            self._items = [str(item) for item in data]
        else:
            self._items = []

    def _save(self) -> None:
        self._storage.write_text(
            json.dumps(self._items, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add(self, item: str) -> None:
        item = item.strip()
        if not item:
            return
        self._items.append(item)
        self._save()

    def remove(self, item: str) -> bool:
        lowered = item.strip().lower()
        for index, current in enumerate(self._items):
            if current.lower() == lowered:
                del self._items[index]
                self._save()
                return True
        return False

    def items(self) -> List[str]:
        return list(self._items)

    def nth(self, index: int) -> str | None:
        if index < 1 or index > len(self._items):
            return None
        return self._items[index - 1]

    def clear(self) -> None:
        self._items = []
        self._save()


__all__ = ["MemoryList"]
```

## `jarwis/speech.py`
```python
"""Entrada de áudio e síntese de voz."""
from __future__ import annotations

import tempfile
from pathlib import Path

import speech_recognition as sr

from .config import AssistantConfig
from .termux import TermuxCommandError, command_available, record_microphone, speak


class SpeechError(RuntimeError):
    """Erro crítico na captura ou síntese de voz."""


class SpeechEngine:
    """Cuida da captura de áudio e da fala do Jarwis."""

    def __init__(self, config: AssistantConfig) -> None:
        self._config = config
        self._recognizer = sr.Recognizer()
        self._recognizer.pause_threshold = 0.8
        self._recognizer.dynamic_energy_threshold = True
        self._backend = self._resolve_backend(config.input_backend)

    def _resolve_backend(self, requested: str) -> str:
        requested = (requested or "auto").lower()
        if requested not in {"auto", "termux", "microphone"}:
            raise SpeechError(f"Backend de áudio desconhecido: {requested}")
        if requested == "termux":
            if not command_available(self._config.termux_microphone_command):
                raise SpeechError(
                    "termux-microphone-record não está disponível. Instale o Termux:API."
                )
            return "termux"
        if requested == "microphone":
            return "microphone"
        if command_available(self._config.termux_microphone_command):
            return "termux"
        return "microphone"

    def listen(self, duration: float) -> str:
        """Captura uma frase e retorna o texto reconhecido."""

        if self._backend == "termux":
            return self._listen_with_termux(duration)
        return self._listen_with_microphone(duration)

    def speak(self, text: str) -> None:
"""Reproduz uma resposta falada (ou faz fallback para o console)."""

        try:
            speak(self._config.termux_tts_command, text)
        except TermuxCommandError:
            print(f"Jarwis: {text}")

    def _listen_with_termux(self, duration: float) -> str:
        destination = Path(tempfile.gettempdir()) / "jarwis-capture.wav"
        try:
            record_microphone(
                self._config.termux_microphone_command,
                destination,
                max(duration, 1.0),
                self._config.sample_rate,
            )
        except TermuxCommandError as exc:
            raise SpeechError(str(exc)) from exc
        try:
            with sr.AudioFile(str(destination)) as source:
                audio = self._recognizer.record(source)
        finally:
            if destination.exists():
                destination.unlink()
        return self._recognize(audio)

    def _listen_with_microphone(self, duration: float) -> str:
        try:
            microphone = sr.Microphone(sample_rate=self._config.sample_rate)
        except Exception as exc:  # pragma: no cover - depende do SO
            raise SpeechError(
                "Não há microfone disponível. Instale o PyAudio ou use o backend Termux."
            ) from exc
        with microphone as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = self._recognizer.listen(source, phrase_time_limit=duration)
        return self._recognize(audio)

    def _recognize(self, audio: sr.AudioData) -> str:
        try:
            text = self._recognizer.recognize_google(audio, language=self._config.language)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:  # pragma: no cover - depende de rede externa
            raise SpeechError(f"Falha na transcrição: {exc}") from exc
        return text.strip()


__all__ = ["SpeechEngine", "SpeechError"]
```

## `jarwis/termux.py`
```python
"""Integrações com Termux:API."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, List


class TermuxCommandError(RuntimeError):
    """Erro ao executar um comando Termux."""

    def __init__(self, command: Iterable[str], stderr: str) -> None:
        self.command = list(command)
        message = f"Falha ao executar {' '.join(self.command)}: {stderr.strip()}"
        super().__init__(message)
        self.stderr = stderr


def command_available(command: str) -> bool:
    """Verifica se um comando Termux está disponível na PATH."""

    return shutil.which(command) is not None


def speak(tts_command: str, text: str) -> None:
    """Fala uma frase usando termux-tts-speak."""

    if not command_available(tts_command):
        raise TermuxCommandError([tts_command], "Comando Termux TTS indisponível")
    result = subprocess.run([tts_command, text], capture_output=True, text=True)
    if result.returncode != 0:
        raise TermuxCommandError([tts_command, text], result.stderr)


def record_microphone(
    command: str,
    destination: Path,
    duration: float,
    sample_rate: int,
) -> None:
    """Grava áudio para ``destination`` usando termux-microphone-record."""

    if not command_available(command):
        raise TermuxCommandError([command], "termux-microphone-record não encontrado")

    attempts: List[List[str]] = []
    for flag in ("-l", "-d", "-e"):
        attempts.append(
            [
                command,
                "-f",
                str(destination),
                flag,
                f"{duration:.2f}",
                "-r",
                str(sample_rate),
            ]
        )
    attempts.append([command, "-f", str(destination), "-r", str(sample_rate)])

    last_error = ""
    for args in attempts:
        try:
            result = subprocess.run(args, capture_output=True, text=True)
        except FileNotFoundError as exc:  # pragma: no cover - depende do ambiente
            raise TermuxCommandError(args, str(exc)) from exc
        if result.returncode == 0:
            return
        last_error = result.stderr
    raise TermuxCommandError(attempts[-1], last_error or "falha ao gravar áudio")


def list_contacts(command: str) -> list[dict[str, object]]:
    """Obtém os contatos disponíveis via termux-contact-list."""

    if not command_available(command):
        raise TermuxCommandError([command], "termux-contact-list não encontrado")
    result = subprocess.run([command], capture_output=True, text=True)
    if result.returncode != 0:
        raise TermuxCommandError([command], result.stderr)
    try:
        data = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:  # pragma: no cover - depende do Termux
        raise TermuxCommandError([command], f"JSON inválido: {exc}") from exc
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def start_phone_call(command: str, number: str) -> None:
    """Inicia uma chamada telefônica usando termux-telephony-call."""

    if not command_available(command):
        raise TermuxCommandError([command, number], "termux-telephony-call não encontrado")
    result = subprocess.run([command, number], capture_output=True, text=True)
    if result.returncode != 0:
        raise TermuxCommandError([command, number], result.stderr)


__all__ = [
    "TermuxCommandError",
    "command_available",
    "speak",
    "record_microphone",
    "list_contacts",
    "start_phone_call",
]
```

## `scripts/termux_service.sh`
```bash
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
```

## `Sistema Jarwis/README.md`
```markdown
# Atalho para a pasta principal

Você está dentro de `Sistema Jarwis`, uma pasta criada automaticamente quando o
Android descompacta o ZIP do projeto. Os arquivos reais ficam **um nível acima**.

- Para usar o projeto daqui, basta executar `python main.py` — este arquivo
  encaminha automaticamente para `../main.py`.
- Os arquivos `requirements*.txt` também encaminham para os do diretório pai.

Apesar disso, o fluxo recomendado é voltar um nível (`cd ..`) e trabalhar
na pasta `Jarwis` original, evitando o espaço no nome do diretório.
```

## `Sistema Jarwis/main.py`
```python
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
runpy.run_path(str(TARGET), run_name="__main__")
```

## `Sistema Jarwis/requirements.txt`
```text
../requirements.txt
```

## `Sistema Jarwis/requirements-desktop.txt`
```text
../requirements-desktop.txt
```
