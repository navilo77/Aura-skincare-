import uuid
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product
from app.modules.product.repositories.base import BaseRepository
from app.modules.product.schemas.product_search_filter import ProductSearchFilter


@dataclass
class _SearchContext:
    search: str | None = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
    skip: int = 0
    limit: int = 20
    brand_id: uuid.UUID | None = None
    category_id: uuid.UUID | None = None
    status: str | None = None
    product_type: str | None = None
    is_active: bool | None = None
    is_featured: bool | None = None
    skin_type_slug: str | None = None
    concern_slug: str | None = None
    ingredient_slug: str | None = None
    benefit_slug: str | None = None
    tag_slug: str | None = None
    routine_slug: str | None = None
    min_price: Decimal | None = None
    max_price: Decimal | None = None

    @classmethod
    def resolve(cls, filters: ProductSearchFilter | None) -> "_SearchContext":
        if filters is None:
            return cls()

        return cls(
            search=filters.search,
            sort_by=filters.sort.value,
            sort_order=filters.sort_order or "desc",
            skip=(filters.page - 1) * filters.limit if filters.page else 0,
            limit=filters.limit,
            brand_id=None,
            category_id=None,
            status=filters.status,
            product_type=filters.product_type,
            is_active=filters.is_active,
            is_featured=filters.is_featured,
            skin_type_slug=filters.skin_type_slug,
            concern_slug=filters.concern_slug,
            ingredient_slug=filters.ingredient_slug,
            benefit_slug=filters.benefit_slug,
            tag_slug=filters.tag_slug,
            routine_slug=filters.routine_slug,
            min_price=filters.price_min,
            max_price=filters.price_max,
        )


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
        filters: ProductSearchFilter | None = None,
    ) -> tuple[list[Product], int]:
        ctx = _SearchContext.resolve(filters)

        if filters is not None:
            if filters.brand_slug is not None:
                from app.modules.product.repositories.brand import BrandRepository

                brand = await BrandRepository(self.session).get_by_slug(
                    filters.brand_slug
                )
                if brand is None:
                    return [], 0
                ctx.brand_id = brand.id

            if filters.category_slug is not None:
                from app.modules.product.repositories.category import CategoryRepository

                category = await CategoryRepository(self.session).get_by_slug(
                    filters.category_slug
                )
                if category is None:
                    return [], 0
                ctx.category_id = category.id

        filter_conditions = []
        if ctx.brand_id is not None:
            filter_conditions.append(Product.brand_id == ctx.brand_id)
        if ctx.category_id is not None:
            filter_conditions.append(Product.category_id == ctx.category_id)
        if ctx.status is not None:
            filter_conditions.append(Product.status == ctx.status)
        if ctx.product_type is not None:
            filter_conditions.append(Product.product_type == ctx.product_type)
        if ctx.is_active is not None:
            filter_conditions.append(Product.is_active == ctx.is_active)
        if ctx.is_featured is not None:
            filter_conditions.append(Product.is_featured == ctx.is_featured)
        if ctx.min_price is not None:
            filter_conditions.append(Product.price >= ctx.min_price)
        if ctx.max_price is not None:
            filter_conditions.append(Product.price <= ctx.max_price)

        if ctx.skin_type_slug is not None:
            from sqlalchemy import select as sa_select

            from app.modules.product.models import ProductSkinType, SkinType

            subquery = (
                sa_select(ProductSkinType.product_id)
                .join(SkinType, ProductSkinType.skin_type_id == SkinType.id)
                .where(SkinType.slug == ctx.skin_type_slug)
            )
            filter_conditions.append(Product.id.in_(subquery))

        if ctx.concern_slug is not None:
            from sqlalchemy import select as sa_select

            from app.modules.product.models import ProductSkinConcern, SkinConcern

            subquery = (
                sa_select(ProductSkinConcern.product_id)
                .join(SkinConcern, ProductSkinConcern.concern_id == SkinConcern.id)
                .where(SkinConcern.slug == ctx.concern_slug)
            )
            filter_conditions.append(Product.id.in_(subquery))

        if ctx.ingredient_slug is not None:
            from sqlalchemy import select as sa_select

            from app.modules.product.models import Ingredient, ProductIngredient

            subquery = (
                sa_select(ProductIngredient.product_id)
                .join(
                    Ingredient, ProductIngredient.ingredient_id == Ingredient.id
                )
                .where(Ingredient.slug == ctx.ingredient_slug)
            )
            filter_conditions.append(Product.id.in_(subquery))

        if ctx.benefit_slug is not None:
            from sqlalchemy import select as sa_select

            from app.modules.product.models import Benefit, ProductBenefit

            subquery = (
                sa_select(ProductBenefit.product_id)
                .join(Benefit, ProductBenefit.benefit_id == Benefit.id)
                .where(Benefit.slug == ctx.benefit_slug)
            )
            filter_conditions.append(Product.id.in_(subquery))

        if ctx.tag_slug is not None:
            from sqlalchemy import select as sa_select

            from app.modules.product.models import ProductTag, Tag

            subquery = (
                sa_select(ProductTag.product_id)
                .join(Tag, ProductTag.tag_id == Tag.id)
                .where(Tag.slug == ctx.tag_slug)
            )
            filter_conditions.append(Product.id.in_(subquery))

        if ctx.routine_slug is not None:
            from sqlalchemy import select as sa_select

            from app.modules.product.models import ProductRoutine, RoutineType

            subquery = (
                sa_select(ProductRoutine.product_id)
                .join(
                    RoutineType, ProductRoutine.routine_type_id == RoutineType.id
                )
                .where(RoutineType.slug == ctx.routine_slug)
            )
            filter_conditions.append(Product.id.in_(subquery))

        query = await self._build_query(
            *filter_conditions,
            search=ctx.search,
            search_fields=["name", "slug", "sku", "short_description"],
        )
        sort_field = getattr(Product, ctx.sort_by, Product.created_at)
        if ctx.sort_order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())

        paginated_query, total = await self._apply_pagination(
            query, ctx.skip, ctx.limit
        )
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
