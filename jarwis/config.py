"""Configurações e utilidades de carregamento do assistente."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass
class AssistantConfig:
    """Parâmetros centrais do Jarwis."""

    wake_word: str = "jarwis"
    alternate_wake_words: tuple[str, ...] = ("jarvis",)
    language: str = "pt-BR"
    passive_listen_seconds: float = 4.0
    command_listen_seconds: float = 6.0
    input_backend: str = "auto"
    sample_rate: int = 16000
    data_dir: Path = field(default_factory=lambda: Path.home() / ".jarwis")
    memory_file: Path = field(init=False)
    contact_refresh_seconds: int = 900
    termux_microphone_command: str = "termux-microphone-record"
    termux_tts_command: str = "termux-tts-speak"
    termux_contact_command: str = "termux-contact-list"
    termux_call_command: str = "termux-telephony-call"

    def __post_init__(self) -> None:
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
