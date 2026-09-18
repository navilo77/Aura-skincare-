from app.modules.inventory.routes.adjustment import router as adjustment_router
from app.modules.inventory.routes.inventory import router as inventory_router
from app.modules.inventory.routes.movement import router as movement_router
from app.modules.inventory.routes.product_supplier import (
    router as product_supplier_router,
)
from app.modules.inventory.routes.reservation import router as reservation_router
from app.modules.inventory.routes.supplier import router as supplier_router
from app.modules.inventory.routes.warehouse import router as warehouse_router

__all__ = [
    "warehouse_router",
    "inventory_router",
    "movement_router",
    "adjustment_router",
    "reservation_router",
    "supplier_router",
    "product_supplier_router",
]
