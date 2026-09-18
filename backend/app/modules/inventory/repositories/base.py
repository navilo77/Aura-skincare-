import uuid
from typing import Any

from sqlalchemy import ColumnElement, Select, delete, func, or_, select
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

    async def exists(self, entity_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.id == entity_id)
        )
        return result.scalar_one() > 0

    async def delete(self, entity_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == entity_id)
        )
        return result.rowcount > 0  # type: ignore[attr-defined, no-any-return]

    async def _build_query(
        self,
        *filters: ColumnElement[bool],
        search: str | None = None,
        search_fields: list[str] | None = None,
    ) -> Select[Any]:
        query = select(self.model).where(*filters)

        if search and search_fields:
            search_conditions = []
            for field_name in search_fields:
                field = getattr(self.model, field_name, None)
                if field is not None:
                    search_conditions.append(field.ilike(f"%{search}%"))
            if search_conditions:
                query = query.where(or_(*search_conditions))

        return query

    async def _apply_pagination(
        self, query: Select[Any], skip: int = 0, limit: int = 20
    ) -> tuple[Select[Any], int]:
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        paginated_query = query.offset(skip).limit(limit)
        return paginated_query, total
