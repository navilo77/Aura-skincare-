import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductIngredient
from app.modules.product.repositories.product_ingredient import (
    ProductIngredientRepository,
)


class ProductIngredientService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductIngredientRepository(session)

    async def link(
        self, product_id: uuid.UUID, ingredient_id: uuid.UUID
    ) -> ProductIngredient:
        link = ProductIngredient(product_id=product_id, ingredient_id=ingredient_id)
        return await self.repository.create(link)

    async def unlink(self, product_id: uuid.UUID, ingredient_id: uuid.UUID) -> None:
        links = await self.repository.get_by_product(product_id)
        for link in links:
            if link.ingredient_id == ingredient_id:
                await self.repository.delete(link.id)

    async def get_product_ingredients(
        self, product_id: uuid.UUID
    ) -> list[ProductIngredient]:
        return await self.repository.get_by_product(product_id)
