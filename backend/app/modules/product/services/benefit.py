import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Benefit
from app.modules.product.repositories.benefit import BenefitRepository


class BenefitService:
    def __init__(self, session: AsyncSession):
        self.repository = BenefitRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> Benefit:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Benefit slug already exists")

        benefit = Benefit(
            name=name,
            slug=slug,
            description=description,
            is_active=True,
        )
        return await self.repository.create(benefit)

    async def update(
        self,
        benefit_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Benefit:
        benefit = await self.repository.get_by_id(benefit_id)
        if not benefit:
            raise ValueError("Benefit not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, benefit_id):
                raise ValueError("Benefit slug already exists")
            benefit.slug = slug

        if name is not None:
            benefit.name = name
        if description is not None:
            benefit.description = description
        if is_active is not None:
            benefit.is_active = is_active

        return await self.repository.update(benefit)

    async def delete(self, benefit_id: uuid.UUID) -> None:
        benefit = await self.repository.get_by_id(benefit_id)
        if not benefit:
            raise ValueError("Benefit not found")
        await self.repository.delete(benefit_id)

    async def get_by_id(self, benefit_id: uuid.UUID) -> Benefit | None:
        return await self.repository.get_by_id(benefit_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Benefit], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
