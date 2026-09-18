import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Supplier
from app.modules.inventory.repositories.base import BaseRepository


class SupplierRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Supplier)

    async def get_by_name(self, name: str) -> Supplier | None:
        result = await self.session.execute(
            select(Supplier).where(Supplier.name == name)
        )
        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        result = await self.session.execute(
            select(Supplier).where(Supplier.name == name)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_name_excluding_id(
        self, name: str, supplier_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Supplier).where(Supplier.name == name, Supplier.id != supplier_id)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, supplier: Supplier) -> Supplier:
        self.session.add(supplier)
        await self.session.flush()
        return supplier

    async def update(self, supplier: Supplier) -> Supplier:
        await self.session.merge(supplier)
        await self.session.flush()
        return supplier
