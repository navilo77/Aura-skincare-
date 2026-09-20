from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import BaseTool


class GetWishlistTool(BaseTool):
    name = "get_wishlist"
    description = "Get the current user's wishlist"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "wishlist": None,
            "message": "Get wishlist requires backend integration",
        }


class GetProfileTool(BaseTool):
    name = "get_profile"
    description = "Get the current user's profile"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "profile": None,
            "message": "Get profile requires backend integration",
        }


class ShippingCostTool(BaseTool):
    name = "shipping_cost"
    description = "Calculate shipping cost for an address"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "cost": None,
            "message": "Shipping cost requires backend integration",
        }


class CouponsTool(BaseTool):
    name = "coupons"
    description = "Get available coupons for the user"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "coupons": [],
            "message": "Get coupons requires backend integration",
        }


class InventoryCheckTool(BaseTool):
    name = "inventory_check"
    description = "Check product stock availability"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "in_stock": False,
            "message": "Inventory check requires backend integration",
        }


class SearchCategoriesTool(BaseTool):
    name = "search_categories"
    description = "Search product categories"

    async def run(self, request: ChatRequest, **kwargs: Any) -> dict[str, Any]:
        return {
            "tool": self.name,
            "categories": [],
            "message": "Search categories requires backend integration",
        }
