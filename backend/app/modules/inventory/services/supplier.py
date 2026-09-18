import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Supplier
from app.modules.inventory.repositories.supplier import SupplierRepository


class SupplierService:
    def __init__(self, session: AsyncSession):
        self.repository = SupplierRepository(session)

    async def create(
        self,
        name: str,
        contact_email: str | None = None,
        contact_phone: str | None = None,
        lead_time_days: int = 0,
        is_active: bool = True,
    ) -> Supplier:
        if await self.repository.exists_by_name(name):
            raise ValueError("Supplier name already exists")

        supplier = Supplier(
            name=name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            lead_time_days=lead_time_days,
            is_active=is_active,
        )
        return await self.repository.create(supplier)

    async def update(
        self,
        supplier_id: uuid.UUID,
        name: str | None = None,
        contact_email: str | None = None,
        contact_phone: str | None = None,
        lead_time_days: int | None = None,
        is_active: bool | None = None,
    ) -> Supplier:
        supplier = await self.repository.get_by_id(supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")

        if name is not None:
            if await self.repository.exists_by_name_excluding_id(name, supplier_id):
                raise ValueError("Supplier name already exists")
            supplier.name = name
        if contact_email is not None:
            supplier.contact_email = contact_email
        if contact_phone is not None:
            supplier.contact_phone = contact_phone
        if lead_time_days is not None:
            supplier.lead_time_days = lead_time_days
        if is_active is not None:
            supplier.is_active = is_active

        return await self.repository.update(supplier)

    async def delete(self, supplier_id: uuid.UUID) -> None:
        supplier = await self.repository.get_by_id(supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")
        await self.repository.delete(supplier_id)

    async def get_by_id(self, supplier_id: uuid.UUID) -> Supplier | None:
        return await self.repository.get_by_id(supplier_id)

    async def get_list(
        self, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> tuple[list[Supplier], int]:
        query = await self.repository._build_query(
            search=search,
            search_fields=["name"],
        )
        query = query.order_by(Supplier.name)
        paginated_query, total = await self.repository._apply_pagination(
            query, skip, limit
        )
        result = await self.repository.session.execute(paginated_query)
        return list(result.scalars().all()), total
