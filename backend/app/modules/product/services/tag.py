import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Tag
from app.modules.product.repositories.tag import TagRepository


class TagService:
    def __init__(self, session: AsyncSession):
        self.repository = TagRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
    ) -> Tag:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Tag slug already exists")

        tag = Tag(
            name=name,
            slug=slug,
            is_active=True,
        )
        return await self.repository.create(tag)

    async def update(
        self,
        tag_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        is_active: bool | None = None,
    ) -> Tag:
        tag = await self.repository.get_by_id(tag_id)
        if not tag:
            raise ValueError("Tag not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, tag_id):
                raise ValueError("Tag slug already exists")
            tag.slug = slug

        if name is not None:
            tag.name = name
        if is_active is not None:
            tag.is_active = is_active

        return await self.repository.update(tag)

    async def delete(self, tag_id: uuid.UUID) -> None:
        tag = await self.repository.get_by_id(tag_id)
        if not tag:
            raise ValueError("Tag not found")
        await self.repository.delete(tag_id)

    async def get_by_id(self, tag_id: uuid.UUID) -> Tag | None:
        return await self.repository.get_by_id(tag_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Tag], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
