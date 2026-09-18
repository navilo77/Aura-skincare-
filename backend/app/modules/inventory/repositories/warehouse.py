import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Warehouse
from app.modules.inventory.repositories.base import BaseRepository


class WarehouseRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Warehouse)

    async def get_by_code(self, code: str) -> Warehouse | None:
        result = await self.session.execute(
            select(Warehouse).where(Warehouse.code == code.upper())
        )
        return result.scalar_one_or_none()

    async def exists_by_code(self, code: str) -> bool:
        result = await self.session.execute(
            select(Warehouse).where(Warehouse.code == code.upper())
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_code_excluding_id(
        self, code: str, warehouse_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Warehouse).where(
                Warehouse.code == code.upper(), Warehouse.id != warehouse_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def create(self, warehouse: Warehouse) -> Warehouse:
        self.session.add(warehouse)
        await self.session.flush()
        return warehouse

    async def update(self, warehouse: Warehouse) -> Warehouse:
        await self.session.merge(warehouse)
        await self.session.flush()
        return warehouse
