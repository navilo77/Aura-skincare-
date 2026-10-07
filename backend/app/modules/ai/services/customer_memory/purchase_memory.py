import uuid
from typing import Any

from app.modules.order.repositories.order import OrderRepository
from app.modules.order.repositories.order_item import OrderItemRepository


class PurchaseMemory:
    def __init__(
        self,
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
    ) -> None:
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository

    async def get_purchase_history(
        self, customer_id: uuid.UUID
    ) -> list[dict[str, Any]]:
        orders, _ = await self.order_repository.get_by_customer(
            customer_id, skip=0, limit=20
        )
        purchase_history: list[dict[str, Any]] = []
        for order in orders:
            items = await self.order_item_repository.get_all_by_order(order.id)
            purchase_history.append(
                {
                    "order_number": order.order_number,
                    "status": order.status,
                    "total_amount": float(order.total_amount),
                    "currency": order.currency,
                    "created_at": (
                        order.created_at.isoformat() if order.created_at else None
                    ),
                    "items": [
                        {
                            "product_name": item.product_name,
                            "quantity": item.quantity,
                            "unit_price": float(item.unit_price),
                            "total_price": float(item.total_price),
                        }
                        for item in items
                    ],
                }
            )
        return purchase_history
