import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductSkinType
from app.modules.product.repositories.product_skin_type import (
    ProductSkinTypeRepository,
)


class ProductSkinTypeService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductSkinTypeRepository(session)

    async def link(
        self, product_id: uuid.UUID, skin_type_id: uuid.UUID
    ) -> ProductSkinType:
        link = ProductSkinType(product_id=product_id, skin_type_id=skin_type_id)
        return await self.repository.create(link)

    async def unlink(self, product_id: uuid.UUID, skin_type_id: uuid.UUID) -> None:
        links = await self.repository.get_by_product(product_id)
        for link in links:
            if link.skin_type_id == skin_type_id:
                await self.repository.delete(link.id)

    async def get_product_skin_types(
        self, product_id: uuid.UUID
    ) -> list[ProductSkinType]:
        return await self.repository.get_by_product(product_id)
