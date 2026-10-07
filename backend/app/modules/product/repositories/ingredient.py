import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Ingredient
from app.modules.product.repositories.base import BaseRepository


class IngredientRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Ingredient)

    async def create(self, ingredient: Ingredient) -> Ingredient:
        self.session.add(ingredient)
        await self.session.flush()
        return ingredient

    async def update(self, ingredient: Ingredient) -> Ingredient:
        await self.session.merge(ingredient)
        await self.session.flush()
        await self.session.refresh(ingredient)
        return ingredient

    async def get_by_id(self, ingredient_id: uuid.UUID) -> Ingredient | None:
        return await super().get_by_id(ingredient_id)

    async def get_by_slug(self, slug: str) -> Ingredient | None:
        result = await self.session.execute(
            select(Ingredient).where(Ingredient.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Ingredient], int]:
        filters = []
        if is_active is not None:
            filters.append(Ingredient.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(Ingredient.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(
            select(Ingredient).where(Ingredient.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, ingredient_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Ingredient).where(
                Ingredient.slug == slug, Ingredient.id != ingredient_id
            )
        )
        return result.scalar_one_or_none() is not None
