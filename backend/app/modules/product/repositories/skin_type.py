import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import SkinType
from app.modules.product.repositories.base import BaseRepository


class SkinTypeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SkinType)

    async def create(self, skin_type: SkinType) -> SkinType:
        self.session.add(skin_type)
        await self.session.flush()
        return skin_type

    async def update(self, skin_type: SkinType) -> SkinType:
        await self.session.merge(skin_type)
        await self.session.flush()
        await self.session.refresh(skin_type)
        return skin_type

    async def get_by_id(self, skin_type_id: uuid.UUID) -> SkinType | None:
        return await super().get_by_id(skin_type_id)

    async def get_by_slug(self, slug: str) -> SkinType | None:
        result = await self.session.execute(
            select(SkinType).where(SkinType.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[SkinType], int]:
        filters = []
        if is_active is not None:
            filters.append(SkinType.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(SkinType.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(
            select(SkinType).where(SkinType.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, skin_type_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(SkinType).where(SkinType.slug == slug, SkinType.id != skin_type_id)
        )
        return result.scalar_one_or_none() is not None
