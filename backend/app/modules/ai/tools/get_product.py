from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import BaseTool


class GetProductTool(BaseTool):
    name = "get_product"
    description = "Get product details by product ID or slug"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "product": None,
            "message": "Get product requires backend integration",
        }
