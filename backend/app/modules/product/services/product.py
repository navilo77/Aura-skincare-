import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product
from app.modules.product.repositories.brand import BrandRepository
from app.modules.product.repositories.category import CategoryRepository
from app.modules.product.repositories.product import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductRepository(session)
        self.brand_repository = BrandRepository(session)
        self.category_repository = CategoryRepository(session)

    async def create(
        self,
        brand_id: uuid.UUID,
        category_id: uuid.UUID,
        name: str,
        slug: str,
        sku: str,
        price: Decimal,
        currency: str,
        short_description: str | None = None,
        description: str | None = None,
        status: str = "draft",
        product_type: str = "simple",
        compare_at_price: Decimal | None = None,
        stock_quantity: int = 0,
        thumbnail_url: str | None = None,
        is_featured: bool = False,
        is_active: bool = True,
    ) -> Product:
        slug = slug.lower()
        sku = sku.upper()

        if await self.repository.exists_by_slug(slug):
            raise ValueError("Product slug already exists")
        if await self.repository.exists_by_sku(sku):
            raise ValueError("Product SKU already exists")

        brand = await self.brand_repository.get_by_id(brand_id)
        if not brand:
            raise ValueError("Brand not found")

        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        product = Product(
            brand_id=brand_id,
            category_id=category_id,
            name=name,
            slug=slug,
            sku=sku,
            short_description=short_description,
            description=description,
            status=status,
            product_type=product_type,
            price=price,
            compare_at_price=compare_at_price,
            currency=currency,
            stock_quantity=stock_quantity,
            thumbnail_url=thumbnail_url,
            is_featured=is_featured,
            is_active=is_active,
        )
        created = await self.repository.create(product)
        return await self.repository.get_with_relations(created.id) or created

    async def update(
        self,
        product_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        sku: str | None = None,
        short_description: str | None = None,
        description: str | None = None,
        status: str | None = None,
        product_type: str | None = None,
        price: Decimal | None = None,
        compare_at_price: Decimal | None = None,
        currency: str | None = None,
        stock_quantity: int | None = None,
        thumbnail_url: str | None = None,
        is_featured: bool | None = None,
        is_active: bool | None = None,
        brand_id: uuid.UUID | None = None,
        category_id: uuid.UUID | None = None,
    ) -> Product:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        if slug is not None:
            slug = slug.lower()
            if await self.repository.exists_by_slug_excluding_id(slug, product_id):
                raise ValueError("Product slug already exists")
            product.slug = slug

        if sku is not None:
            sku = sku.upper()
            if await self.repository.exists_by_sku_excluding_id(sku, product_id):
                raise ValueError("Product SKU already exists")
            product.sku = sku

        if name is not None:
            product.name = name
        if short_description is not None:
            product.short_description = short_description
        if description is not None:
            product.description = description
        if status is not None:
            product.status = status
        if product_type is not None:
            product.product_type = product_type
        if price is not None:
            product.price = price
        if compare_at_price is not None:
            product.compare_at_price = compare_at_price  # type: ignore[assignment]
        if currency is not None:
            product.currency = currency
        if stock_quantity is not None:
            product.stock_quantity = stock_quantity
        if thumbnail_url is not None:
            product.thumbnail_url = thumbnail_url
        if is_featured is not None:
            product.is_featured = is_featured
        if is_active is not None:
            product.is_active = is_active

        if brand_id is not None:
            brand = await self.brand_repository.get_by_id(brand_id)
            if not brand:
                raise ValueError("Brand not found")
            product.brand_id = brand_id

        if category_id is not None:
            category = await self.category_repository.get_by_id(category_id)
            if not category:
                raise ValueError("Category not found")
            product.category_id = category_id

        updated = await self.repository.update(product)
        return await self.repository.get_with_relations(updated.id) or updated

    async def delete(self, product_id: uuid.UUID) -> None:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        await self.repository.delete(product_id)

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        return await self.repository.get_with_relations(product_id)

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
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            brand_id=brand_id,
            category_id=category_id,
            status=status,
            product_type=product_type,
            is_active=is_active,
            is_featured=is_featured,
            min_price=min_price,
            max_price=max_price,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def get_featured(self, skip: int = 0, limit: int = 20) -> list[Product]:
        return await self.repository.get_featured(skip=skip, limit=limit)

    async def get_by_brand(
        self,
        brand_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        return await self.repository.get_by_brand(
            brand_id, skip=skip, limit=limit
        )

    async def get_by_category(
        self,
        category_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        return await self.repository.get_by_category(
            category_id, skip=skip, limit=limit
        )
