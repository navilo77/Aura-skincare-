import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductTag
from app.modules.product.repositories.base import BaseRepository


class ProductTagRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductTag)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductTag]:
        result = await self.session.execute(
            select(ProductTag).where(ProductTag.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_tag(self, tag_id: uuid.UUID) -> list[ProductTag]:
        result = await self.session.execute(
            select(ProductTag).where(ProductTag.tag_id == tag_id)
        )
        return list(result.scalars().all())
