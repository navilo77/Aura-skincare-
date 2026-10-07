import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductSkinType
from app.modules.product.repositories.base import BaseRepository


class ProductSkinTypeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductSkinType)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductSkinType]:
        result = await self.session.execute(
            select(ProductSkinType).where(ProductSkinType.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_skin_type(self, skin_type_id: uuid.UUID) -> list[ProductSkinType]:
        result = await self.session.execute(
            select(ProductSkinType).where(ProductSkinType.skin_type_id == skin_type_id)
        )
        return list(result.scalars().all())
