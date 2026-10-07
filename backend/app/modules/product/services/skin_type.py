import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import SkinType
from app.modules.product.repositories.skin_type import SkinTypeRepository


class SkinTypeService:
    def __init__(self, session: AsyncSession):
        self.repository = SkinTypeRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> SkinType:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Skin type slug already exists")

        skin_type = SkinType(
            name=name,
            slug=slug,
            description=description,
            is_active=True,
        )
        return await self.repository.create(skin_type)

    async def update(
        self,
        skin_type_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> SkinType:
        skin_type = await self.repository.get_by_id(skin_type_id)
        if not skin_type:
            raise ValueError("Skin type not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, skin_type_id):
                raise ValueError("Skin type slug already exists")
            skin_type.slug = slug

        if name is not None:
            skin_type.name = name
        if description is not None:
            skin_type.description = description
        if is_active is not None:
            skin_type.is_active = is_active

        return await self.repository.update(skin_type)

    async def delete(self, skin_type_id: uuid.UUID) -> None:
        skin_type = await self.repository.get_by_id(skin_type_id)
        if not skin_type:
            raise ValueError("Skin type not found")
        await self.repository.delete(skin_type_id)

    async def get_by_id(self, skin_type_id: uuid.UUID) -> SkinType | None:
        return await self.repository.get_by_id(skin_type_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[SkinType], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
