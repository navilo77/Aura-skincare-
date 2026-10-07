from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import BaseTool
from app.modules.product.schemas.product_search_filter import ProductSearchFilter
from app.modules.product.services.product import ProductService


class SearchProductsTool(BaseTool):
    name = "search_products"
    description = "Search for products in the catalog by query string"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        db_session = kwargs.get("db")
        query = request.message.strip()

        if not db_session:
            return {
                "tool": self.name,
                "results": [],
                "total": 0,
                "message": "Database session not available",
            }

        service = ProductService(db_session)
        products, total = await service.get_list(
            ProductSearchFilter(search=query or None),
        )

        if total == 0:
            return {
                "tool": self.name,
                "results": [],
                "total": 0,
            }

        results = [
            {
                "id": str(p.id),
                "name": p.name,
                "price": float(p.price) if p.price else None,
                "is_active": p.is_active,
                "description": p.description,
            }
            for p in products
        ]

        return {
            "tool": self.name,
            "query": request.message,
            "results": results,
            "total": total,
            "message": f"{total} products found",
        }
