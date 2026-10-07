import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductSkinConcern
from app.modules.product.repositories.product_skin_concern import (
    ProductSkinConcernRepository,
)


class ProductSkinConcernService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductSkinConcernRepository(session)

    async def link(
        self, product_id: uuid.UUID, concern_id: uuid.UUID
    ) -> ProductSkinConcern:
        link = ProductSkinConcern(product_id=product_id, concern_id=concern_id)
        return await self.repository.create(link)

    async def unlink(self, product_id: uuid.UUID, concern_id: uuid.UUID) -> None:
        links = await self.repository.get_by_product(product_id)
        for link in links:
            if link.concern_id == concern_id:
                await self.repository.delete(link.id)

    async def get_product_concerns(
        self, product_id: uuid.UUID
    ) -> list[ProductSkinConcern]:
        return await self.repository.get_by_product(product_id)
