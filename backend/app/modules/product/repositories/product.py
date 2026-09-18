import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product
from app.modules.product.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()
        return product

    async def update(self, product: Product) -> Product:
        await self.session.merge(product)
        await self.session.flush()
        return product

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        return await super().get_by_id(product_id)

    async def get_with_relations(self, product_id: uuid.UUID) -> Product | None:
        from sqlalchemy import select as sa_select
        from sqlalchemy.orm import selectinload
        result = await self.session.execute(
            sa_select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.brand), selectinload(Product.category))
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        brand_id: uuid.UUID | None = None,
        category_id: uuid.UUID | None = None,
        status: str | None = None,
        product_type: str | None = None,
        is_active: bool | None = None,
        is_featured: bool | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Product], int]:
        filters = []
        if brand_id is not None:
            filters.append(Product.brand_id == brand_id)
        if category_id is not None:
            filters.append(Product.category_id == category_id)
        if status is not None:
            filters.append(Product.status == status)
        if product_type is not None:
            filters.append(Product.product_type == product_type)
        if is_active is not None:
            filters.append(Product.is_active == is_active)
        if is_featured is not None:
            filters.append(Product.is_featured == is_featured)
        if min_price is not None:
            filters.append(Product.price >= min_price)
        if max_price is not None:
            filters.append(Product.price <= max_price)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["name", "slug", "sku", "short_description"],
        )
        sort_field = getattr(Product, sort_by, Product.created_at)
        if sort_order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.session.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none() is not None

    async def exists_by_slug_excluding_id(
        self, slug: str, product_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(Product).where(Product.slug == slug, Product.id != product_id)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_sku(self, sku: str) -> bool:
        result = await self.session.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none() is not None

    async def exists_by_sku_excluding_id(self, sku: str, product_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(Product).where(Product.sku == sku, Product.id != product_id)
        )
        return result.scalar_one_or_none() is not None

    async def get_featured(self, skip: int = 0, limit: int = 20) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .where(Product.is_featured, Product.is_active)
            .order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_brand(
        self, brand_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .where(Product.brand_id == brand_id)
            .order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_category(
        self, category_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .where(Product.category_id == category_id)
            .order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
