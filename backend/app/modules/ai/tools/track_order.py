from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import BaseTool


class TrackOrderTool(BaseTool):
    name = "track_order"
    description = "Track an order by order ID"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "order": None,
            "message": "Track order requires backend integration",
        }
