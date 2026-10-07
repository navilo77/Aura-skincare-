from __future__ import annotations

from typing import Any

from app.modules.ai.memory.redis_session_store import RedisSessionStore


class MemoryManager:
    def __init__(self, session_store: RedisSessionStore) -> None:
        self._session_store = session_store

    async def load(self, session_id: str) -> list[dict[str, Any]]:
        data = await self._session_store.get(session_id)
        if data is None:
            return []
        return data.get("history", [])

    async def save(self, session_id: str, data: dict[str, Any]) -> None:
        await self._session_store.set(session_id, data)

    async def append_conversation(
        self, session_id: str, role: str, content: str
    ) -> None:
        await self._session_store.append_message(session_id, role, content)

    async def clear(self, session_id: str) -> None:
        await self._session_store.clear(session_id)

    async def load_customer_memory(self, customer_id: str) -> dict[str, Any]:
        return {}

    async def save_customer_memory(
        self, customer_id: str, data: dict[str, Any]
    ) -> None:
        return None
