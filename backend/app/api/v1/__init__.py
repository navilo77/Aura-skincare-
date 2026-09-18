from fastapi import APIRouter

from app.modules.analytics.routes.analytics import router as analytics_router
from app.modules.analytics.routes.event import router as event_router
from app.modules.auth.routes.auth import router as auth_router
from app.modules.auth.routes.role import router as role_router
from app.modules.customer.routes.customer import router as customer_router
from app.modules.inventory.routes.adjustment import router as adjustment_router
from app.modules.inventory.routes.inventory import router as inventory_router
from app.modules.inventory.routes.movement import router as movement_router
from app.modules.inventory.routes.product_supplier import (
    router as product_supplier_router,
)
from app.modules.inventory.routes.reservation import router as reservation_router
from app.modules.inventory.routes.supplier import router as supplier_router
from app.modules.inventory.routes.warehouse import router as warehouse_router
from app.modules.notification.routes.notification import router as notification_router
from app.modules.order.routes.billing_address import router as billing_address_router
from app.modules.order.routes.order import router as order_router
from app.modules.order.routes.order_item import router as order_item_router
from app.modules.order.routes.shipping_address import router as shipping_address_router
from app.modules.product.routes.brand import router as brand_router
from app.modules.product.routes.category import router as category_router
from app.modules.product.routes.product import router as product_router
from app.modules.product.routes.product_image import router as product_image_router
from app.modules.product.routes.product_variant import router as product_variant_router

router = APIRouter()

router.include_router(
    notification_router, prefix="/notifications", tags=["notifications"]
)
router.include_router(event_router, prefix="/analytics", tags=["analytics-events"])
router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(role_router, prefix="/auth", tags=["roles"])
router.include_router(customer_router, prefix="/customers", tags=["customers"])
router.include_router(
    warehouse_router, prefix="/inventory/warehouses", tags=["warehouses"]
)
router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
router.include_router(
    movement_router, prefix="/inventory/movements", tags=["inventory-movements"]
)
router.include_router(
    adjustment_router, prefix="/inventory/adjustments", tags=["inventory-adjustments"]
)
router.include_router(
    reservation_router,
    prefix="/inventory/reservations",
    tags=["inventory-reservations"],
)
router.include_router(
    supplier_router, prefix="/inventory/suppliers", tags=["suppliers"]
)
router.include_router(
    product_supplier_router, prefix="/inventory", tags=["product-suppliers"]
)
router.include_router(brand_router, prefix="/products", tags=["brands"])
router.include_router(category_router, prefix="/products", tags=["categories"])
router.include_router(
    product_image_router, prefix="/products", tags=["product-images"]
)
router.include_router(
    product_variant_router, prefix="/products", tags=["product-variants"]
)
router.include_router(product_router, prefix="/products", tags=["products"])
router.include_router(order_router, prefix="/orders", tags=["orders"])
router.include_router(
    order_item_router, prefix="/orders/{order_id}", tags=["order-items"]
)
router.include_router(
    shipping_address_router, prefix="/orders/{order_id}", tags=["shipping-addresses"]
)
router.include_router(
    billing_address_router, prefix="/orders/{order_id}", tags=["billing-addresses"]
)
