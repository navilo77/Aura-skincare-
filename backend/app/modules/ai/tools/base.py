from abc import ABC, abstractmethod
from typing import Any

from app.modules.ai.schemas.ai import ChatRequest


class BaseTool(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        pass


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[BaseTool]:
        return list(self._tools.values())
