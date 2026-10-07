import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import SkinConcern
from app.modules.product.repositories.skin_concern import SkinConcernRepository


class SkinConcernService:
    def __init__(self, session: AsyncSession):
        self.repository = SkinConcernRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> SkinConcern:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Skin concern slug already exists")

        skin_concern = SkinConcern(
            name=name,
            slug=slug,
            description=description,
            is_active=True,
        )
        return await self.repository.create(skin_concern)

    async def update(
        self,
        skin_concern_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> SkinConcern:
        skin_concern = await self.repository.get_by_id(skin_concern_id)
        if not skin_concern:
            raise ValueError("Skin concern not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, skin_concern_id):
                raise ValueError("Skin concern slug already exists")
            skin_concern.slug = slug

        if name is not None:
            skin_concern.name = name
        if description is not None:
            skin_concern.description = description
        if is_active is not None:
            skin_concern.is_active = is_active

        return await self.repository.update(skin_concern)

    async def delete(self, skin_concern_id: uuid.UUID) -> None:
        skin_concern = await self.repository.get_by_id(skin_concern_id)
        if not skin_concern:
            raise ValueError("Skin concern not found")
        await self.repository.delete(skin_concern_id)

    async def get_by_id(self, skin_concern_id: uuid.UUID) -> SkinConcern | None:
        return await self.repository.get_by_id(skin_concern_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[SkinConcern], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
