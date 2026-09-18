import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Inventory
from app.modules.inventory.repositories.inventory import InventoryRepository
from app.modules.inventory.repositories.warehouse import WarehouseRepository


class InventoryService:
    def __init__(self, session: AsyncSession):
        self.repository = InventoryRepository(session)
        self.warehouse_repository = WarehouseRepository(session)

    async def create(
        self,
        product_id: uuid.UUID,
        warehouse_id: uuid.UUID,
        quantity_on_hand: int = 0,
        quantity_reserved: int = 0,
        low_stock_threshold: int = 10,
        is_tracking_enabled: bool = True,
    ) -> Inventory:
        if quantity_reserved > quantity_on_hand:
            raise ValueError("quantity_reserved cannot exceed quantity_on_hand")

        warehouse = await self.warehouse_repository.get_by_id(warehouse_id)
        if not warehouse:
            raise ValueError("Warehouse not found")

        existing = await self.repository.get_by_product(product_id)
        if existing:
            raise ValueError("Inventory record already exists for this product")

        inventory = Inventory(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity_on_hand=quantity_on_hand,
            quantity_reserved=quantity_reserved,
            low_stock_threshold=low_stock_threshold,
            is_tracking_enabled=is_tracking_enabled,
        )
        return await self.repository.create(inventory)

    async def update(
        self,
        product_id: uuid.UUID,
        low_stock_threshold: int | None = None,
        is_tracking_enabled: bool | None = None,
    ) -> Inventory:
        inventory = await self.repository.get_by_product(product_id)
        if not inventory:
            raise ValueError("Inventory not found")

        if low_stock_threshold is not None:
            inventory.low_stock_threshold = low_stock_threshold
        if is_tracking_enabled is not None:
            inventory.is_tracking_enabled = is_tracking_enabled

        return await self.repository.update(inventory)

    async def get_by_product(self, product_id: uuid.UUID) -> Inventory | None:
        return await self.repository.get_by_product(product_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        warehouse_id: uuid.UUID | None = None,
        low_stock_only: bool = False,
    ) -> tuple[list[Inventory], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            warehouse_id=warehouse_id,
            low_stock_only=low_stock_only,
        )

    async def delete(self, product_id: uuid.UUID) -> None:
        inventory = await self.repository.get_by_product(product_id)
        if not inventory:
            raise ValueError("Inventory not found")
        await self.repository.delete(inventory.id)
