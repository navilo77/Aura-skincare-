import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Tag
from app.modules.product.repositories.base import BaseRepository


class TagRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tag)

    async def create(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        return tag

    async def update(self, tag: Tag) -> Tag:
        await self.session.merge(tag)
        await self.session.flush()
        await self.session.refresh(tag)
        return tag

    async def get_by_id(self, tag_id: uuid.UUID) -> Tag | None:
        return await super().get_by_id(tag_id)

    async def get_by_slug(self, slug: str) -> Tag | None:
        result = await self.session.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Tag], int]:
        filters = []
        if is_active is not None:
            filters.append(Tag.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(Tag.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(self, slug: str, tag_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(Tag).where(Tag.slug == slug, Tag.id != tag_id)
        )
        return result.scalar_one_or_none() is not None
