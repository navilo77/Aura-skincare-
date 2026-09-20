from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import BaseTool


class SearchProductsTool(BaseTool):
    name = "search_products"
    description = "Search for products by query string"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        query = request.message
        return {
            "tool": self.name,
            "query": query,
            "results": [],
            "message": "Product search requires backend integration",
        }
