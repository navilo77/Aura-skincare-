from __future__ import annotations

import logging
from typing import Protocol

import httpx

logger = logging.getLogger(__name__)


class AIProvider(Protocol):
    async def generate(self, prompt: str) -> str | None: ...


class GeminiProvider:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        model: str = "gemini-2.0-flash",
        timeout: float = 10.0,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    async def generate(self, prompt: str) -> str | None:
        if not self._api_key:
            return None

        url = (
            f"{self._base_url}/models/{self._model}:generateContent?key={self._api_key}"
        )
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                res = await client.post(
                    url,
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                )
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text_val = parts[0].get("text")
                            if isinstance(text_val, str) and text_val.strip():
                                return text_val.strip()
                else:
                    logger.warning(
                        "Gemini API non-200 response: %s %s",
                        res.status_code,
                        res.text,
                    )
        except Exception as e:
            logger.error("Gemini API error: %s", e)
        return None
