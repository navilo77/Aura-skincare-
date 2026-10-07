import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import SkinConcern
from app.modules.product.repositories.base import BaseRepository


class SkinConcernRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SkinConcern)

    async def create(self, skin_concern: SkinConcern) -> SkinConcern:
        self.session.add(skin_concern)
        await self.session.flush()
        return skin_concern

    async def update(self, skin_concern: SkinConcern) -> SkinConcern:
        await self.session.merge(skin_concern)
        await self.session.flush()
        await self.session.refresh(skin_concern)
        return skin_concern

    async def get_by_id(self, skin_concern_id: uuid.UUID) -> SkinConcern | None:
        return await super().get_by_id(skin_concern_id)

    async def get_by_slug(self, slug: str) -> SkinConcern | None:
        result = await self.session.execute(
            select(SkinConcern).where(SkinConcern.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[SkinConcern], int]:
        filters = []
        if is_active is not None:
            filters.append(SkinConcern.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(SkinConcern.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(
            select(SkinConcern).where(SkinConcern.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, skin_concern_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(SkinConcern).where(
                SkinConcern.slug == slug, SkinConcern.id != skin_concern_id
            )
        )
        return result.scalar_one_or_none() is not None
