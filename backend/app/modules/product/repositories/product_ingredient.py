import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductIngredient
from app.modules.product.repositories.base import BaseRepository


class ProductIngredientRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductIngredient)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductIngredient]:
        result = await self.session.execute(
            select(ProductIngredient).where(ProductIngredient.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_ingredient(
        self, ingredient_id: uuid.UUID
    ) -> list[ProductIngredient]:
        result = await self.session.execute(
            select(ProductIngredient).where(
                ProductIngredient.ingredient_id == ingredient_id
            )
        )
        return list(result.scalars().all())
