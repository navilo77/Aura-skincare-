import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Category
from app.modules.product.repositories.category import CategoryRepository


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repository = CategoryRepository(session)

    async def create(
        self,
        name: str,
        slug: str,
        parent_id: uuid.UUID | None = None,
        description: str | None = None,
        image_url: str | None = None,
        sort_order: int = 0,
    ) -> Category:
        slug = slug.lower()
        if await self.repository.exists_by_slug(slug):
            raise ValueError("Category slug already exists")

        if parent_id is not None:
            parent = await self.repository.get_by_id(parent_id)
            if not parent:
                raise ValueError("Parent category not found")

        category = Category(
            parent_id=parent_id,
            name=name,
            slug=slug,
            description=description,
            image_url=image_url,
            sort_order=sort_order,
            is_active=True,
        )
        return await self.repository.create(category)

    async def update(
        self,
        category_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        parent_id: uuid.UUID | None = None,
        description: str | None = None,
        image_url: str | None = None,
        sort_order: int | None = None,
        is_active: bool | None = None,
    ) -> Category:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, category_id):
                raise ValueError("Category slug already exists")
            category.slug = slug

        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        if image_url is not None:
            category.image_url = image_url
        if sort_order is not None:
            category.sort_order = sort_order
        if is_active is not None:
            category.is_active = is_active

        if parent_id is not None:
            if parent_id == category_id:
                raise ValueError("Category cannot be its own parent")
            parent = await self.repository.get_by_id(parent_id)
            if not parent:
                raise ValueError("Parent category not found")
            category.parent_id = parent_id
        else:
            category.parent_id = None

        return await self.repository.update(category)

    async def delete(self, category_id: uuid.UUID) -> None:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        children = await self.repository.get_children(category_id)
        if children:
            raise ValueError("Cannot delete category with child categories")

        await self.repository.delete(category_id)

    async def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        return await self.repository.get_by_id(category_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        parent_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Category], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            parent_id=parent_id,
            is_active=is_active,
            search=search,
        )

    async def get_children(self, parent_id: uuid.UUID) -> list[Category]:
        return await self.repository.get_children(parent_id)
