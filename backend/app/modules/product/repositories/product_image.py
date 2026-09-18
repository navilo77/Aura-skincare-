import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductImage
from app.modules.product.repositories.base import BaseRepository


class ProductImageRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductImage)

    async def create(self, image: ProductImage) -> ProductImage:
        self.session.add(image)
        await self.session.flush()
        return image

    async def update(self, image: ProductImage) -> ProductImage:
        await self.session.merge(image)
        await self.session.flush()
        await self.session.refresh(image)
        return image

    async def get_by_id(self, image_id: uuid.UUID) -> ProductImage | None:
        return await super().get_by_id(image_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        product_id: uuid.UUID | None = None,
        is_primary: bool | None = None,
    ) -> tuple[list[ProductImage], int]:
        filters = []
        if product_id is not None:
            filters.append(ProductImage.product_id == product_id)
        if is_primary is not None:
            filters.append(ProductImage.is_primary == is_primary)

        query = select(ProductImage).where(*filters)
        query = query.order_by(ProductImage.sort_order, ProductImage.created_at)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_by_product(
        self, product_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[ProductImage]:
        result = await self.session.execute(
            select(ProductImage)
            .where(ProductImage.product_id == product_id)
            .order_by(ProductImage.sort_order, ProductImage.created_at)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_primary(self, product_id: uuid.UUID) -> ProductImage | None:
        result = await self.session.execute(
            select(ProductImage).where(
                ProductImage.product_id == product_id,
                ProductImage.is_primary,
            )
        )
        return result.scalar_one_or_none()

    async def delete(self, image_id: uuid.UUID) -> bool:
        return await super().delete(image_id)

    async def delete_by_product(self, product_id: uuid.UUID) -> int:
        result = await self.session.execute(
            delete(ProductImage).where(ProductImage.product_id == product_id)
        )
        return result.rowcount  # type: ignore[attr-defined, no-any-return]
