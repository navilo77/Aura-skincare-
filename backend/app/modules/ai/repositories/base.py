import uuid
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession, model: type[Any]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, entity_id: uuid.UUID) -> Any | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, field_name: str, value: Any) -> Any | None:
        field = getattr(self.model, field_name, None)
        if field is None:
            return None
        result = await self.session.execute(
            select(self.model).where(field == value)
        )
        return result.scalar_one_or_none()

    async def exists_by_field(self, field_name: str, value: Any) -> bool:
        field = getattr(self.model, field_name, None)
        if field is None:
            return False
        result = await self.session.execute(
            select(func.count(self.model.id)).where(field == value)
        )
        return result.scalar_one() > 0

    async def get_list_by_field(self, field_name: str, value: Any) -> list[Any]:
        field = getattr(self.model, field_name, None)
        if field is None:
            return []
        result = await self.session.execute(
            select(self.model).where(field == value)
        )
        return list(result.scalars().all())

    async def get_list_by_filters(self, filters: dict[str, Any]) -> list[Any]:
        query = select(self.model)
        for field_name, value in filters.items():
            field = getattr(self.model, field_name, None)
            if field is not None:
                query = query.where(field == value)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def exists(self, entity_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.id == entity_id)
        )
        return result.scalar_one() > 0

    async def create(self, entity: Any) -> Any:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: Any, **kwargs: Any) -> Any:
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == entity_id)
        )
        return result.rowcount > 0

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        **filters: Any,
    ) -> tuple[list[Any], int]:
        query = select(self.model)
        for field_name, value in filters.items():
            field = getattr(self.model, field_name, None)
            if field is not None:
                query = query.where(field == value)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        paginated_query = query.offset(skip).limit(limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total
