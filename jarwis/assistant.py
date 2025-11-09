"""Orquestração principal do Jarwis."""
from __future__ import annotations

import logging
from typing import Optional

from .commands import ParsedCommand, parse_command
from .config import AssistantConfig
from .contacts import ContactBook
from .memory import MemoryList
from .speech import SpeechEngine, SpeechError

logger = logging.getLogger(__name__)


class JarwisAssistant:
    """Assistente de voz que reage ao chamado "Jarwis"."""

    def __init__(self, config: Optional[AssistantConfig] = None) -> None:
        self.config = config or AssistantConfig()
        self.speech = SpeechEngine(self.config)
        self.memory = MemoryList(self.config.memory_file)
        self.contacts = ContactBook(self.config)

    def run(self, loop_once: bool = False) -> None:
        """Inicia o laço principal de escuta."""

        logger.info("Assistente iniciado com wake words: %s", ", ".join(self.config.wake_words))
        try:
            while True:
                heard = self.speech.listen(self.config.passive_listen_seconds)
                if not heard:
                    if loop_once:
                        break
                    continue
                logger.debug("Transcrição passiva: %s", heard)
                if not self._is_wake_word_present(heard):
                    if loop_once:
                        break
                    continue
                self.speech.speak("Senhor, o que deseja?")
                command_text = self.speech.listen(self.config.command_listen_seconds)
                if not command_text:
                    self.speech.speak("Não ouvi nenhum pedido, senhor.")
                    if loop_once:
                        break
                    continue
                logger.info("Comando reconhecido: %s", command_text)
                response = self._handle_command(command_text)
                              if response:
                    self.speech.speak(response)
                if loop_once:
                    break
        except KeyboardInterrupt:
            logger.info("Jarwis interrompido pelo usuário.")
        except SpeechError as exc:
            logger.error("Erro de áudio: %s", exc)
            raise

    def _is_wake_word_present(self, text: str) -> bool:
        lowered = text.lower()
        return any(word in lowered for word in self.config.wake_words)

    def _handle_command(self, command_text: str) -> str:
        parsed = parse_command(command_text)
        if parsed is None:
            return "Ainda não sei como fazer isso, senhor."
        if parsed.action == "call":
            return self._handle_call(parsed)
        if parsed.action == "add" and parsed.text:
            self.memory.add(parsed.text)
            return f"Adicionei {parsed.text} à lista, senhor."
        if parsed.action == "list_all":
            items = self.memory.items()
            if not items:
                return "A lista está vazia, senhor."
            itens_formatados = ", ".join(items)
            return f"Na lista estão: {itens_formatados}."
        if parsed.action == "nth" and parsed.index:
            item = self.memory.nth(parsed.index)
            if item is None:
                return "Ainda não tenho tantos itens assim na lista, senhor."
            return f"O {parsed.index}º termo da lista é {item}."
        if parsed.action == "remove" and parsed.text:
            removed = self.memory.remove(parsed.text)
            if not removed:
                return "Senhor, isso não tem na lista."
            return f"Retirei {parsed.text} da lista, senhor."
        return "Ainda não sei como fazer isso, senhor."

    def _handle_call(self, parsed: ParsedCommand) -> str:
        if not parsed.text:
            return "Preciso saber para quem ligar, senhor."
        contact = self.contacts.find(parsed.text)
        if contact is None:
            return f"Não encontrei {parsed.text} nos contatos, senhor."
        if not self.contacts.call(contact):
            return "Não consegui iniciar a chamada, senhor."
        return f"Ligando para {contact.name}."


__all__ = ["JarwisAssistant"]
