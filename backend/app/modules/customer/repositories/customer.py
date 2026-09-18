import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customer.models import Customer
from app.modules.customer.repositories.base import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Customer)

    async def create(self, customer: Customer) -> Customer:
        self.session.add(customer)
        await self.session.flush()
        return customer

    async def update(self, customer: Customer) -> Customer:
        await self.session.merge(customer)
        await self.session.flush()
        await self.session.refresh(customer)
        return customer

    async def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        return await super().get_by_id(customer_id)

    async def get_by_email(self, email: str) -> Customer | None:
        result = await self.session.execute(
            select(Customer).where(Customer.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Customer | None:
        result = await self.session.execute(
            select(Customer).where(Customer.phone == phone)
        )
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(Customer).where(Customer.email == email)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_email_excluding_id(
        self, email: str, customer_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Customer).where(Customer.email == email, Customer.id != customer_id)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_phone(self, phone: str) -> bool:
        result = await self.session.execute(
            select(Customer).where(Customer.phone == phone)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_phone_excluding_id(
        self, phone: str, customer_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Customer).where(Customer.phone == phone, Customer.id != customer_id)
        )
        return result.scalar_one_or_none() is not None

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Customer], int]:
        filters = []
        if status is not None:
            filters.append(Customer.status == status)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["full_name", "email", "phone"],
        )
        query = query.order_by(Customer.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total
