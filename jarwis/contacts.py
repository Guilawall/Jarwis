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
