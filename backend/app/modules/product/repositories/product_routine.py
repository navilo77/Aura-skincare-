import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductRoutine
from app.modules.product.repositories.base import BaseRepository


class ProductRoutineRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductRoutine)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductRoutine]:
        result = await self.session.execute(
            select(ProductRoutine).where(ProductRoutine.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_routine_type(
        self, routine_type_id: uuid.UUID
    ) -> list[ProductRoutine]:
        result = await self.session.execute(
            select(ProductRoutine).where(
                ProductRoutine.routine_type_id == routine_type_id
            )
        )
        return list(result.scalars().all())
