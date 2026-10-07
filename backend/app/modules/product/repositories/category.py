import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Category
from app.modules.product.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Category)

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        return category

    async def update(self, category: Category) -> Category:
        await self.session.merge(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        return await super().get_by_id(category_id)

    async def get_by_slug(self, slug: str) -> Category | None:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        parent_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Category], int]:
        filters = []
        if parent_id is not None:
            filters.append(Category.parent_id == parent_id)
        if is_active is not None:
            filters.append(Category.is_active == is_active)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug"],
        )
        query = query.order_by(Category.sort_order, Category.name)

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_children(self, parent_id: uuid.UUID) -> list[Category]:
        result = await self.session.execute(
            select(Category).where(Category.parent_id == parent_id)
        )
        return list(result.scalars().all())

    async def get_all_with_children(self) -> list[Category]:
        from sqlalchemy import select as sa_select
        from sqlalchemy.orm import selectinload

        result = await self.session.execute(
            sa_select(Category).options(selectinload(Category.children))
        )
        return list(result.scalars().all())

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, category_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug, Category.id != category_id)
        )
        return result.scalar_one_or_none() is not None
