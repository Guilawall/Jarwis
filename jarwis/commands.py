 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/jarwis/commands.py b/jarwis/commands.py
new file mode 100644
index 0000000000000000000000000000000000000000..bc424247823153f3d1cd475ecca0b23ec3dbef2d
--- /dev/null
+++ b/jarwis/commands.py
@@ -0,0 +1,168 @@
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
 
EOF
)
