import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductVariant
from app.modules.product.repositories.base import BaseRepository


class ProductVariantRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductVariant)

    async def create(self, variant: ProductVariant) -> ProductVariant:
        self.session.add(variant)
        await self.session.flush()
        return variant

    async def update(self, variant: ProductVariant) -> ProductVariant:
        await self.session.merge(variant)
        await self.session.flush()
        await self.session.refresh(variant)
        return variant

    async def get_by_id(self, variant_id: uuid.UUID) -> ProductVariant | None:
        return await super().get_by_id(variant_id)

    async def get_by_sku(self, sku: str) -> ProductVariant | None:
        result = await self.session.execute(
            select(ProductVariant).where(ProductVariant.sku == sku)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        product_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[ProductVariant], int]:
        filters = []
        if product_id is not None:
            filters.append(ProductVariant.product_id == product_id)
        if is_active is not None:
            filters.append(ProductVariant.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "sku"],
        )
        query = query.order_by(ProductVariant.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_by_product(
        self, product_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[ProductVariant]:
        result = await self.session.execute(
            select(ProductVariant)
            .where(ProductVariant.product_id == product_id)
            .order_by(ProductVariant.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def exists_by_sku(self, sku: str) -> bool:
        result = await self.session.execute(
            select(ProductVariant).where(ProductVariant.sku == sku)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_sku_excluding_id(self, sku: str, variant_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(ProductVariant).where(
                ProductVariant.sku == sku, ProductVariant.id != variant_id
            )
        )
        return result.scalar_one_or_none() is not None
