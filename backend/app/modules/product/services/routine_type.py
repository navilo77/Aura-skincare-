import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import RoutineType
from app.modules.product.repositories.routine_type import RoutineTypeRepository


class RoutineTypeService:
    def __init__(self, session: AsyncSession):
        self.repository = RoutineTypeRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> RoutineType:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Routine type slug already exists")

        routine_type = RoutineType(
            name=name,
            slug=slug,
            description=description,
            is_active=True,
        )
        return await self.repository.create(routine_type)

    async def update(
        self,
        routine_type_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> RoutineType:
        routine_type = await self.repository.get_by_id(routine_type_id)
        if not routine_type:
            raise ValueError("Routine type not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, routine_type_id):
                raise ValueError("Routine type slug already exists")
            routine_type.slug = slug

        if name is not None:
            routine_type.name = name
        if description is not None:
            routine_type.description = description
        if is_active is not None:
            routine_type.is_active = is_active

        return await self.repository.update(routine_type)

    async def delete(self, routine_type_id: uuid.UUID) -> None:
        routine_type = await self.repository.get_by_id(routine_type_id)
        if not routine_type:
            raise ValueError("Routine type not found")
        await self.repository.delete(routine_type_id)

    async def get_by_id(self, routine_type_id: uuid.UUID) -> RoutineType | None:
        return await self.repository.get_by_id(routine_type_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[RoutineType], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
