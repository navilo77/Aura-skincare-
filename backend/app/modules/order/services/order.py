import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import BillingAddress, Order, OrderItem, ShippingAddress
from app.modules.order.repositories.billing_address import BillingAddressRepository
from app.modules.order.repositories.order import OrderRepository
from app.modules.order.repositories.order_item import OrderItemRepository
from app.modules.order.repositories.shipping_address import ShippingAddressRepository
from app.modules.product.repositories.product import ProductRepository


class OrderService:
    VALID_TRANSITIONS = {
        "pending": ["processing", "cancelled"],
        "processing": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": [],
    }

    def __init__(self, session: AsyncSession):
        self.repository = OrderRepository(session)
        self.item_repository = OrderItemRepository(session)
        self.shipping_address_repository = ShippingAddressRepository(session)
        self.billing_address_repository = BillingAddressRepository(session)
        self.product_repository = ProductRepository(session)

    async def _generate_order_number(self) -> str:
        while True:
            timestamp = datetime.now(UTC).strftime("%y%m%d%H%M%S")
            random_part = str(uuid.uuid4().int)[:4]
            order_number = f"ORD-{timestamp}-{random_part}"
            existing = await self.repository.get_by_order_number(order_number)
            if not existing:
                return order_number

    async def create(
        self,
        customer_id: uuid.UUID,
        items: list[Any],
        shipping_address: dict[str, Any] | None = None,
        billing_address: dict[str, Any] | None = None,
        currency: str = "USD",
        status: str = "pending",
    ) -> Order:
        # TODO: Validate customer exists when Customer module is available
        if not items:
            raise ValueError("Order must have at least one item")

        normalized_items = []
        for item in items:
            if hasattr(item, "model_dump"):
                normalized_items.append(item.model_dump())
            elif hasattr(item, "dict"):
                normalized_items.append(item.dict())
            else:
                normalized_items.append(dict(item))

        total_amount = Decimal("0.00")
        for item in normalized_items:
            product_id = uuid.UUID(str(item.get("product_id")))
            quantity = item.get("quantity", 0)
            unit_price = item.get("unit_price")

            if not product_id:
                raise ValueError("product_id is required for each item")
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            if not product.is_active:
                raise ValueError(f"Product {product_id} is not active")
            if product.stock_quantity < quantity:
                raise ValueError(f"Insufficient stock for product {product_id}")

            if unit_price is None:
                unit_price = Decimal(str(product.price))
            total_amount += Decimal(str(unit_price)) * Decimal(str(quantity))

        order_number = await self._generate_order_number()
        order = Order(
            customer_id=customer_id,
            order_number=order_number,
            status=status,
            total_amount=total_amount,
            currency=currency,
        )
        created_order = await self.repository.create(order)

        for item in normalized_items:
            product_id = uuid.UUID(str(item["product_id"]))
            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            order_item = OrderItem(
                order_id=created_order.id,
                product_id=product_id,
                quantity=item["quantity"],
                unit_price=Decimal(str(product.price)),
                total_price=Decimal(str(product.price))
                * Decimal(str(item["quantity"])),
                product_name=product.name,
                sku=product.sku,
                variant_name=item.get("variant_name"),
            )
            await self.item_repository.create(order_item)

        if shipping_address:
            shipping = ShippingAddress(
                order_id=created_order.id,
                full_name=shipping_address["full_name"],
                phone=shipping_address["phone"],
                address_line1=shipping_address["address_line1"],
                address_line2=shipping_address.get("address_line2"),
                city=shipping_address["city"],
                state=shipping_address["state"],
                postal_code=shipping_address["postal_code"],
                country=shipping_address["country"],
            )
            await self.shipping_address_repository.create(shipping)

        if billing_address:
            billing = BillingAddress(
                order_id=created_order.id,
                full_name=billing_address["full_name"],
                phone=billing_address["phone"],
                address_line1=billing_address["address_line1"],
                address_line2=billing_address.get("address_line2"),
                city=billing_address["city"],
                state=billing_address["state"],
                postal_code=billing_address["postal_code"],
                country=billing_address["country"],
            )
            await self.billing_address_repository.create(billing)

        return (
            await self.repository.get_with_relations(uuid.UUID(str(created_order.id)))
            or created_order
        )

    async def update(self, order_id: uuid.UUID, status: str | None = None) -> Order:
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        if status is not None:
            allowed = self.VALID_TRANSITIONS.get(order.status, [])
            if status not in allowed:
                raise ValueError(f"Cannot transition from {order.status} to {status}")
            order.status = status

        updated = await self.repository.update(order)
        return (
            await self.repository.get_with_relations(uuid.UUID(str(updated.id)))
            or updated
        )

    async def delete(self, order_id: uuid.UUID) -> None:
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        if order.status in ("delivered", "cancelled"):
            raise ValueError("Cannot delete completed orders")

        shipping = await self.shipping_address_repository.get_shipping_address(order_id)
        if shipping:
            await self.shipping_address_repository.delete(uuid.UUID(str(shipping.id)))

        billing = await self.billing_address_repository.get_billing_address(order_id)
        if billing:
            await self.billing_address_repository.delete(uuid.UUID(str(billing.id)))

        await self.repository.delete(order_id)

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        return await self.repository.get_with_relations(order_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        customer_id: uuid.UUID | None = None,
        status: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Order], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            customer_id=customer_id,
            status=status,
            search=search,
        )
