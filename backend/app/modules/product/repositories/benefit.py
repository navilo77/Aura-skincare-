import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Benefit
from app.modules.product.repositories.base import BaseRepository


class BenefitRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Benefit)

    async def create(self, benefit: Benefit) -> Benefit:
        self.session.add(benefit)
        await self.session.flush()
        return benefit

    async def update(self, benefit: Benefit) -> Benefit:
        await self.session.merge(benefit)
        await self.session.flush()
        await self.session.refresh(benefit)
        return benefit

    async def get_by_id(self, benefit_id: uuid.UUID) -> Benefit | None:
        return await super().get_by_id(benefit_id)

    async def get_by_slug(self, slug: str) -> Benefit | None:
        result = await self.session.execute(select(Benefit).where(Benefit.slug == slug))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Benefit], int]:
        filters = []
        if is_active is not None:
            filters.append(Benefit.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(Benefit.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(select(Benefit).where(Benefit.slug == slug))
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, benefit_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Benefit).where(Benefit.slug == slug, Benefit.id != benefit_id)
        )
        return result.scalar_one_or_none() is not None
