from abc import ABC, abstractmethod
from typing import Any

from app.modules.ai.schemas.ai import ChatRequest, ChatResponse


class BaseAgent(ABC):
    name: str = ""

    @abstractmethod
    async def handle(self, request: ChatRequest, **kwargs: Any) -> ChatResponse:
        pass
