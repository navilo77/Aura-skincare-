from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import BaseTool


class GetCartTool(BaseTool):
    name = "get_cart"
    description = "Get the current user's shopping cart"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "cart": None,
            "message": "Get cart requires backend integration",
        }
