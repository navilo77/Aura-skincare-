import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductImage
from app.modules.product.repositories.product import ProductRepository
from app.modules.product.repositories.product_image import ProductImageRepository


class ProductImageService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductImageRepository(session)
        self.product_repository = ProductRepository(session)

    async def create(
        self,
        product_id: uuid.UUID,
        image_url: str,
        alt_text: str | None = None,
        sort_order: int = 0,
        is_primary: bool = False,
    ) -> ProductImage:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        image = ProductImage(
            product_id=product_id,
            image_url=image_url,
            alt_text=alt_text,
            sort_order=sort_order,
            is_primary=is_primary,
        )
        return await self.repository.create(image)

    async def update(
        self,
        image_id: uuid.UUID,
        image_url: str | None = None,
        alt_text: str | None = None,
        sort_order: int | None = None,
        is_primary: bool | None = None,
    ) -> ProductImage:
        image = await self.repository.get_by_id(image_id)
        if not image:
            raise ValueError("Product image not found")

        if image_url is not None:
            image.image_url = image_url
        if alt_text is not None:
            image.alt_text = alt_text
        if sort_order is not None:
            image.sort_order = sort_order
        if is_primary is not None:
            image.is_primary = is_primary

        return await self.repository.update(image)

    async def delete(self, image_id: uuid.UUID) -> None:
        image = await self.repository.get_by_id(image_id)
        if not image:
            raise ValueError("Product image not found")
        await self.repository.delete(image_id)

    async def get_by_id(self, image_id: uuid.UUID) -> ProductImage | None:
        return await self.repository.get_by_id(image_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        product_id: uuid.UUID | None = None,
        is_primary: bool | None = None,
    ) -> tuple[list[ProductImage], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            product_id=product_id,
            is_primary=is_primary,
        )

    async def get_by_product(
        self,
        product_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[ProductImage]:
        return await self.repository.get_by_product(product_id, skip=skip, limit=limit)

    async def get_primary(self, product_id: uuid.UUID) -> ProductImage | None:
        return await self.repository.get_primary(product_id)

    async def delete_by_product(self, product_id: uuid.UUID) -> int:
        return await self.repository.delete_by_product(product_id)
