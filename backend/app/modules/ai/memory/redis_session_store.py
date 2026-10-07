from __future__ import annotations

import json
from typing import Any

from app.integrations.redis import redis_client


class RedisSessionStore:
    def __init__(self, prefix: str = "ai:session", ttl: int = 86400) -> None:
        self._prefix = prefix
        self._ttl = ttl

    def _key(self, session_id: str) -> str:
        return f"{self._prefix}:{session_id}"

    async def _get_data(self, session_id: str) -> dict[str, Any] | None:
        key = self._key(session_id)
        raw = await redis_client.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, AttributeError):
            return None

    async def _set_data(self, session_id: str, data: dict[str, Any]) -> None:
        key = self._key(session_id)
        await redis_client.set(key, json.dumps(data), ex=self._ttl)

    async def get(self, session_id: str) -> dict[str, Any] | None:
        return await self._get_data(session_id)

    async def set(self, session_id: str, data: dict[str, Any]) -> None:
        await self._set_data(session_id, data)

    async def append_message(self, session_id: str, role: str, content: str) -> None:
        data = await self._get_data(session_id)
        if data is None:
            data = {}
        history = data.get("history", [])
        history.append({"role": role, "content": content})
        if len(history) > 50:
            history = history[-50:]
        data["history"] = history
        await self._set_data(session_id, data)

    async def clear(self, session_id: str) -> None:
        await redis_client.delete(self._key(session_id))
