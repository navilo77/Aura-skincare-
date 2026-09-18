from fastapi import APIRouter

from app.modules.order.routes.billing_address import router as billing_address_router
from app.modules.order.routes.order import router as order_router
from app.modules.order.routes.order_item import router as order_item_router
from app.modules.order.routes.shipping_address import router as shipping_address_router

router = APIRouter()

router.include_router(order_router, prefix="/orders", tags=["orders"])
router.include_router(order_item_router, prefix="/orders", tags=["order-items"])
router.include_router(
    shipping_address_router, prefix="/orders", tags=["shipping-addresses"]
)
router.include_router(
    billing_address_router, prefix="/orders", tags=["billing-addresses"]
)
