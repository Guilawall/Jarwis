 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/jarwis/memory.py b/jarwis/memory.py
new file mode 100644
index 0000000000000000000000000000000000000000..5a06d44b59cc434c08f0905e6fbd2b5e51eef14c
--- /dev/null
+++ b/jarwis/memory.py
@@ -0,0 +1,66 @@
+"""Persistência da lista solicitada pelo usuário."""
+from __future__ import annotations
+
+import json
+from pathlib import Path
+from typing import List
+
+
+class MemoryList:
+    """Gerencia a lista personalizada do usuário."""
+
+    def __init__(self, storage: Path) -> None:
+        self._storage = storage
+        self._storage.parent.mkdir(parents=True, exist_ok=True)
+        self._items: List[str] = []
+        self._load()
+
+    def _load(self) -> None:
+        if not self._storage.exists():
+            self._items = []
+            return
+        try:
+            data = json.loads(self._storage.read_text(encoding="utf-8"))
+        except json.JSONDecodeError:
+            self._items = []
+            return
+        if isinstance(data, list):
+            self._items = [str(item) for item in data]
+        else:
+            self._items = []
+
+    def _save(self) -> None:
+        self._storage.write_text(
+            json.dumps(self._items, ensure_ascii=False, indent=2), encoding="utf-8"
+        )
+
+    def add(self, item: str) -> None:
+        item = item.strip()
+        if not item:
+            return
+        self._items.append(item)
+        self._save()
+
+    def remove(self, item: str) -> bool:
+        lowered = item.strip().lower()
+        for index, current in enumerate(self._items):
+            if current.lower() == lowered:
+                del self._items[index]
+                self._save()
+                return True
+        return False
+
+    def items(self) -> List[str]:
+        return list(self._items)
+
+    def nth(self, index: int) -> str | None:
+        if index < 1 or index > len(self._items):
+            return None
+        return self._items[index - 1]
+
+    def clear(self) -> None:
+        self._items = []
+        self._save()
+
+
+__all__ = ["MemoryList"]
 
EOF
)
