import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Inventory
from app.modules.inventory.repositories.base import BaseRepository


class InventoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Inventory)

    async def get_by_product(self, product_id: uuid.UUID) -> Inventory | None:
        result = await self.session.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_warehouse(self, warehouse_id: uuid.UUID) -> list[Inventory]:
        result = await self.session.execute(
            select(Inventory).where(Inventory.warehouse_id == warehouse_id)
        )
        return list(result.scalars().all())

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        warehouse_id: uuid.UUID | None = None,
        low_stock_only: bool = False,
    ) -> tuple[list[Inventory], int]:
        filters = []
        if warehouse_id is not None:
            filters.append(Inventory.warehouse_id == warehouse_id)
        if low_stock_only:
            filters.append(
                Inventory.quantity_on_hand - Inventory.quantity_reserved
                <= Inventory.low_stock_threshold
            )

        query = await self._build_query(*filters)
        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def create(self, inventory: Inventory) -> Inventory:
        self.session.add(inventory)
        await self.session.flush()
        return inventory

    async def update(self, inventory: Inventory) -> Inventory:
        await self.session.merge(inventory)
        await self.session.flush()
        return inventory
