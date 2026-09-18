import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import BillingAddress
from app.modules.order.repositories.billing_address import BillingAddressRepository
from app.modules.order.repositories.order import OrderRepository


class BillingAddressService:
    def __init__(self, session: AsyncSession):
        self.repository = BillingAddressRepository(session)
        self.order_repository = OrderRepository(session)

    async def create(
        self,
        order_id: uuid.UUID,
        full_name: str,
        phone: str,
        address_line1: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
        address_line2: str | None = None,
    ) -> BillingAddress:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        address = BillingAddress(
            order_id=order_id,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
        )
        return await self.repository.create(address)

    async def update(
        self,
        address_id: uuid.UUID,
        full_name: str | None = None,
        phone: str | None = None,
        address_line1: str | None = None,
        address_line2: str | None = None,
        city: str | None = None,
        state: str | None = None,
        postal_code: str | None = None,
        country: str | None = None,
    ) -> BillingAddress:
        address = await self.repository.get_by_id(address_id)
        if not address:
            raise ValueError("Billing address not found")

        if full_name is not None:
            address.full_name = full_name
        if phone is not None:
            address.phone = phone
        if address_line1 is not None:
            address.address_line1 = address_line1
        if address_line2 is not None:
            address.address_line2 = address_line2
        if city is not None:
            address.city = city
        if state is not None:
            address.state = state
        if postal_code is not None:
            address.postal_code = postal_code
        if country is not None:
            address.country = country

        return await self.repository.update(address)

    async def delete(self, address_id: uuid.UUID) -> None:
        address = await self.repository.get_by_id(address_id)
        if not address:
            raise ValueError("Billing address not found")
        await self.repository.delete(address_id)

    async def get_by_id(self, address_id: uuid.UUID) -> BillingAddress | None:
        return await self.repository.get_by_id(address_id)

    async def get_list(
        self, skip: int = 0, limit: int = 20, order_id: uuid.UUID | None = None
    ) -> tuple[list[BillingAddress], int]:
        return await self.repository.get_list(skip=skip, limit=limit, order_id=order_id)

    async def get_billing_address(self, order_id: uuid.UUID) -> BillingAddress | None:
        return await self.repository.get_billing_address(order_id)
