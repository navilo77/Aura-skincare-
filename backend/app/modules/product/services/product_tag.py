import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductTag
from app.modules.product.repositories.product_tag import (
    ProductTagRepository,
)


class ProductTagService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductTagRepository(session)

    async def link(self, product_id: uuid.UUID, tag_id: uuid.UUID) -> ProductTag:
        link = ProductTag(product_id=product_id, tag_id=tag_id)
        return await self.repository.create(link)

    async def unlink(self, product_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        links = await self.repository.get_by_product(product_id)
        for link in links:
            if link.tag_id == tag_id:
                await self.repository.delete(link.id)

    async def get_product_tags(self, product_id: uuid.UUID) -> list[ProductTag]:
        return await self.repository.get_by_product(product_id)
