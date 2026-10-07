from __future__ import annotations

import logging

import httpx

from app.config.settings import settings
from app.modules.ai.services.rag.exceptions import EmbeddingServiceError

logger = logging.getLogger(__name__)

_MAX_RETRIES = 2
_EMBEDDING_TIMEOUT = 30.0


class EmbeddingService:
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = _EMBEDDING_TIMEOUT,
        max_retries: int = _MAX_RETRIES,
    ) -> None:
        self._base_url = (base_url or settings.ollama_url).rstrip("/")
        self._model = model or settings.ollama_embedding_model
        self._timeout = timeout
        self._max_retries = max_retries

    async def embed(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise EmbeddingServiceError("Cannot embed empty text")

        results = await self._call_ollama([text])
        return results[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        valid = [t.strip() for t in texts if t and t.strip()]
        if not valid:
            return []

        results: list[list[float]] = []
        for i in range(0, len(valid), 10):
            batch = valid[i : i + 10]
            batch_results = await self._call_ollama(batch)
            results.extend(batch_results)

        return results

    async def _call_ollama(self, prompts: list[str]) -> list[list[float]]:
        url = f"{self._base_url}/api/embeddings"
        payload = {"model": self._model, "prompt": prompts}

        last_error: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        if len(prompts) == 1:
                            embedding = data.get("embedding", [])
                            if not embedding:
                                raise EmbeddingServiceError(
                                    "Ollama returned empty embedding"
                                )
                            return [list(embedding)]

                        embeddings = data.get("embeddings", [])
                        if len(embeddings) != len(prompts):
                            raise EmbeddingServiceError(
                                f"Expected {len(prompts)} embeddings, "
                                f"got {len(embeddings)}"
                            )
                        return [list(e) for e in embeddings]

                    logger.warning(
                        "Ollama non-200 on attempt %s/%s: %s %s",
                        attempt,
                        self._max_retries,
                        response.status_code,
                        response.text[:200],
                    )
                    last_error = EmbeddingServiceError(
                        f"Ollama returned {response.status_code}"
                    )
            except EmbeddingServiceError:
                raise
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Ollama embedding attempt %s/%s failed: %s",
                    attempt,
                    self._max_retries,
                    exc,
                )

        raise EmbeddingServiceError(
            f"Embedding generation failed after {self._max_retries} "
            f"retries: {last_error}"
        )

    @property
    def model_name(self) -> str:
        return self._model
