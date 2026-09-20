from __future__ import annotations

from typing import Any


class SessionMemory:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def get(self, session_id: str) -> dict[str, Any] | None:
        return self._store.get(session_id)

    def set(self, session_id: str, data: dict[str, Any]) -> None:
        self._store[session_id] = data

    def append_message(self, session_id: str, role: str, content: str) -> None:
        session = self._store.setdefault(session_id, {})
        history = session.setdefault("history", [])
        history.append({"role": role, "content": content})
        if len(history) > 50:
            session["history"] = history[-50:]

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)
