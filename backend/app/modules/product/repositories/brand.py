import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Brand
from app.modules.product.repositories.base import BaseRepository


class BrandRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Brand)

    async def create(self, brand: Brand) -> Brand:
        self.session.add(brand)
        await self.session.flush()
        return brand

    async def update(self, brand: Brand) -> Brand:
        await self.session.merge(brand)
        await self.session.flush()
        await self.session.refresh(brand)
        return brand

    async def get_by_id(self, brand_id: uuid.UUID) -> Brand | None:
        return await super().get_by_id(brand_id)

    async def get_by_slug(self, slug: str) -> Brand | None:
        result = await self.session.execute(select(Brand).where(Brand.slug == slug))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Brand], int]:
        filters = []
        if is_active is not None:
            filters.append(Brand.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(Brand.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(select(Brand).where(Brand.slug == slug))
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(self, slug: str, brand_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(Brand).where(Brand.slug == slug, Brand.id != brand_id)
        )
        return result.scalar_one_or_none() is not None
