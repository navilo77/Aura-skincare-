import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductRoutine
from app.modules.product.repositories.product_routine import (
    ProductRoutineRepository,
)


class ProductRoutineService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductRoutineRepository(session)

    async def link(
        self, product_id: uuid.UUID, routine_type_id: uuid.UUID
    ) -> ProductRoutine:
        link = ProductRoutine(product_id=product_id, routine_type_id=routine_type_id)
        return await self.repository.create(link)

    async def unlink(self, product_id: uuid.UUID, routine_type_id: uuid.UUID) -> None:
        links = await self.repository.get_by_product(product_id)
        for link in links:
            if link.routine_type_id == routine_type_id:
                await self.repository.delete(link.id)

    async def get_product_routines(self, product_id: uuid.UUID) -> list[ProductRoutine]:
        return await self.repository.get_by_product(product_id)
