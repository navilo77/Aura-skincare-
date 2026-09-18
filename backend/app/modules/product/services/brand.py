import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Brand
from app.modules.product.repositories.brand import BrandRepository


class BrandService:
    def __init__(self, session: AsyncSession):
        self.repository = BrandRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        description: str | None = None,
        logo_url: str | None = None,
    ) -> Brand:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Brand slug already exists")

        brand = Brand(
            name=name,
            slug=slug,
            description=description,
            logo_url=logo_url,
            is_active=True,
        )
        return await self.repository.create(brand)

    async def update(
        self,
        brand_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        logo_url: str | None = None,
        is_active: bool | None = None,
    ) -> Brand:
        brand = await self.repository.get_by_id(brand_id)
        if not brand:
            raise ValueError("Brand not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, brand_id):
                raise ValueError("Brand slug already exists")
            brand.slug = slug

        if name is not None:
            brand.name = name
        if description is not None:
            brand.description = description
        if logo_url is not None:
            brand.logo_url = logo_url
        if is_active is not None:
            brand.is_active = is_active

        return await self.repository.update(brand)

    async def delete(self, brand_id: uuid.UUID) -> None:
        brand = await self.repository.get_by_id(brand_id)
        if not brand:
            raise ValueError("Brand not found")
        await self.repository.delete(brand_id)

    async def get_by_id(self, brand_id: uuid.UUID) -> Brand | None:
        return await self.repository.get_by_id(brand_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Brand], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
