import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryMovement
from app.modules.inventory.repositories.inventory import InventoryRepository
from app.modules.inventory.repositories.movement import InventoryMovementRepository


class MovementService:
    POSITIVE_TYPES = {"purchase", "return", "transfer_in", "adjustment"}
    NEGATIVE_TYPES = {"sale", "transfer_out"}

    def __init__(self, session: AsyncSession):
        self.repository = InventoryMovementRepository(session)
        self.inventory_repository = InventoryRepository(session)

    async def create(
        self,
        inventory_id: uuid.UUID,
        movement_type: str,
        quantity: int,
        reference_type: str | None = None,
        reference_id: uuid.UUID | None = None,
        notes: str | None = None,
        actor_id: uuid.UUID | None = None,
    ) -> InventoryMovement:
        inventory = await self.inventory_repository.get_by_id(inventory_id)
        if not inventory:
            raise ValueError("Inventory not found")

        if movement_type in self.POSITIVE_TYPES and quantity <= 0:
            raise ValueError(
                f"quantity must be positive for movement type '{movement_type}'"
            )
        if movement_type in self.NEGATIVE_TYPES and quantity >= 0:
            raise ValueError(
                f"quantity must be negative for movement type '{movement_type}'"
            )

        movement = InventoryMovement(
            inventory_id=inventory_id,
            movement_type=movement_type,
            quantity=quantity,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
        )
        return await self.repository.create(movement)

    async def get_by_inventory(
        self, inventory_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[InventoryMovement], int]:
        return await self.repository.get_by_inventory(
            inventory_id, skip=skip, limit=limit
        )

    async def get_by_reference(
        self, reference_type: str, reference_id: uuid.UUID
    ) -> list[InventoryMovement]:
        return await self.repository.get_by_reference(reference_type, reference_id)
