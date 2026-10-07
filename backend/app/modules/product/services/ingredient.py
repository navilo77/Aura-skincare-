import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Ingredient
from app.modules.product.repositories.ingredient import IngredientRepository


class IngredientService:
    def __init__(self, session: AsyncSession):
        self.repository = IngredientRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> Ingredient:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Ingredient slug already exists")

        ingredient = Ingredient(
            name=name,
            slug=slug,
            description=description,
            is_active=True,
        )
        return await self.repository.create(ingredient)

    async def update(
        self,
        ingredient_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Ingredient:
        ingredient = await self.repository.get_by_id(ingredient_id)
        if not ingredient:
            raise ValueError("Ingredient not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, ingredient_id):
                raise ValueError("Ingredient slug already exists")
            ingredient.slug = slug

        if name is not None:
            ingredient.name = name
        if description is not None:
            ingredient.description = description
        if is_active is not None:
            ingredient.is_active = is_active

        return await self.repository.update(ingredient)

    async def delete(self, ingredient_id: uuid.UUID) -> None:
        ingredient = await self.repository.get_by_id(ingredient_id)
        if not ingredient:
            raise ValueError("Ingredient not found")
        await self.repository.delete(ingredient_id)

    async def get_by_id(self, ingredient_id: uuid.UUID) -> Ingredient | None:
        return await self.repository.get_by_id(ingredient_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Ingredient], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            is_active=is_active,
            search=search,
        )
