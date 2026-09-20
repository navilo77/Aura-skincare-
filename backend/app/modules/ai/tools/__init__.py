from app.modules.ai.tools.base import BaseTool as BaseTool
from app.modules.ai.tools.base import ToolRegistry
from app.modules.ai.tools.get_cart import GetCartTool
from app.modules.ai.tools.get_product import GetProductTool
from app.modules.ai.tools.misc_tools import (
    CouponsTool,
    GetProfileTool,
    GetWishlistTool,
    InventoryCheckTool,
    SearchCategoriesTool,
    ShippingCostTool,
)
from app.modules.ai.tools.search_products import SearchProductsTool
from app.modules.ai.tools.track_order import TrackOrderTool


def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(SearchProductsTool())
    registry.register(GetProductTool())
    registry.register(GetCartTool())
    registry.register(GetWishlistTool())
    registry.register(GetProfileTool())
    registry.register(TrackOrderTool())
    registry.register(ShippingCostTool())
    registry.register(CouponsTool())
    registry.register(InventoryCheckTool())
    registry.register(SearchCategoriesTool())
    return registry
