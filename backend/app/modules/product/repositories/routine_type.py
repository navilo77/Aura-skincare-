import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import RoutineType
from app.modules.product.repositories.base import BaseRepository


class RoutineTypeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RoutineType)

    async def create(self, routine_type: RoutineType) -> RoutineType:
        self.session.add(routine_type)
        await self.session.flush()
        return routine_type

    async def update(self, routine_type: RoutineType) -> RoutineType:
        await self.session.merge(routine_type)
        await self.session.flush()
        await self.session.refresh(routine_type)
        return routine_type

    async def get_by_id(self, routine_type_id: uuid.UUID) -> RoutineType | None:
        return await super().get_by_id(routine_type_id)

    async def get_by_slug(self, slug: str) -> RoutineType | None:
        result = await self.session.execute(
            select(RoutineType).where(RoutineType.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[RoutineType], int]:
        filters = []
        if is_active is not None:
            filters.append(RoutineType.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(RoutineType.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(
            select(RoutineType).where(RoutineType.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, routine_type_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(RoutineType).where(
                RoutineType.slug == slug, RoutineType.id != routine_type_id
            )
        )
        return result.scalar_one_or_none() is not None
