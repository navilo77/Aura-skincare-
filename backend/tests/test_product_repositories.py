import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductVariant,
)
from app.modules.product.repositories.brand import BrandRepository
from app.modules.product.repositories.category import CategoryRepository
from app.modules.product.repositories.product import ProductRepository
from app.modules.product.repositories.product_image import ProductImageRepository
from app.modules.product.repositories.product_variant import ProductVariantRepository


@pytest.mark.asyncio
async def test_brand_repository_crud(db_session: AsyncSession):
    repo = BrandRepository(db_session)
    brand = Brand(name="Test Brand", slug="test-brand", description="A test brand")
    db_session.add(brand)
    await db_session.flush()

    fetched = await repo.get_by_id(brand.id)
    assert fetched is not None
    assert fetched.name == "Test Brand"
    assert fetched.slug == "test-brand"

    brand.name = "Updated Brand"
    updated = await repo.update(brand)
    assert updated.name == "Updated Brand"

    assert await repo.exists_by_slug("test-brand") is True
    assert await repo.exists_by_slug("nonexistent") is False

    await repo.delete(brand.id)
    assert await repo.get_by_id(brand.id) is None


@pytest.mark.asyncio
async def test_brand_repository_duplicate_slug(db_session: AsyncSession):
    repo = BrandRepository(db_session)
    brand = Brand(name="Brand A", slug="brand-a")
    db_session.add(brand)
    await db_session.flush()

    assert await repo.exists_by_slug("brand-a") is True
    assert await repo.exists_by_slug_excluding_id("brand-a", uuid.uuid4()) is True


@pytest.mark.asyncio
async def test_category_repository_crud(db_session: AsyncSession):
    repo = CategoryRepository(db_session)
    category = Category(name="Test Category", slug="test-category")
    db_session.add(category)
    await db_session.flush()

    fetched = await repo.get_by_id(category.id)
    assert fetched is not None
    assert fetched.name == "Test Category"

    category.name = "Updated Category"
    updated = await repo.update(category)
    assert updated.name == "Updated Category"

    await repo.delete(category.id)
    assert await repo.get_by_id(category.id) is None


@pytest.mark.asyncio
async def test_category_repository_children(db_session: AsyncSession):
    repo = CategoryRepository(db_session)
    parent = Category(name="Parent", slug="parent")
    db_session.add(parent)
    await db_session.flush()

    child = Category(name="Child", slug="child", parent_id=parent.id)
    db_session.add(child)
    await db_session.flush()

    children = await repo.get_children(parent.id)
    assert len(children) == 1
    assert children[0].id == child.id


@pytest.mark.asyncio
async def test_product_repository_crud(db_session: AsyncSession):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    repo = ProductRepository(db_session)
    product = Product(
        brand_id=brand.id,
        category_id=category.id,
        name="Test Product",
        slug="test-product",
        sku="SKU-001",
        price=10.00,
    )
    db_session.add(product)
    await db_session.flush()

    fetched = await repo.get_by_id(product.id)
    assert fetched is not None
    assert fetched.name == "Test Product"

    product.name = "Updated Product"
    updated = await repo.update(product)
    assert updated.name == "Updated Product"

    assert await repo.exists_by_slug("test-product") is True
    assert await repo.exists_by_sku("SKU-001") is True

    await repo.delete(product.id)
    assert await repo.get_by_id(product.id) is None


@pytest.mark.asyncio
async def test_product_repository_get_by_brand_and_category(db_session: AsyncSession):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    repo = ProductRepository(db_session)
    product = Product(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-1",
        price=10.00,
    )
    db_session.add(product)
    await db_session.flush()

    by_brand = await repo.get_by_brand(brand.id)
    assert len(by_brand) == 1

    by_category = await repo.get_by_category(category.id)
    assert len(by_category) == 1


@pytest.mark.asyncio
async def test_product_repository_pagination_and_search(db_session: AsyncSession):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    repo = ProductRepository(db_session)
    for i in range(5):
        product = Product(
            brand_id=brand.id,
            category_id=category.id,
            name=f"Product {i}",
            slug=f"product-{i}",
            sku=f"SKU-{i}",
            price=10.00 + i,
        )
        db_session.add(product)
    await db_session.flush()

    products, total = await repo.get_list(skip=0, limit=2)
    assert len(products) == 2
    assert total == 5

    products, total = await repo.get_list(search="Product 1")
    assert total == 1
    assert products[0].name == "Product 1"


@pytest.mark.asyncio
async def test_product_image_repository_crud(db_session: AsyncSession):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    product = Product(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-1",
        price=10.00,
    )
    db_session.add(product)
    await db_session.flush()

    repo = ProductImageRepository(db_session)
    image = ProductImage(product_id=product.id, image_url="http://example.com/img.jpg")
    db_session.add(image)
    await db_session.flush()

    fetched = await repo.get_by_id(image.id)
    assert fetched is not None
    assert fetched.image_url == "http://example.com/img.jpg"

    images = await repo.get_by_product(product.id)
    assert len(images) == 1

    await repo.delete(image.id)
    assert await repo.get_by_id(image.id) is None


@pytest.mark.asyncio
async def test_product_variant_repository_crud(db_session: AsyncSession):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    product = Product(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-1",
        price=10.00,
    )
    db_session.add(product)
    await db_session.flush()

    repo = ProductVariantRepository(db_session)
    variant = ProductVariant(
        product_id=product.id,
        name="Variant",
        sku="VAR-001",
        price=15.00,
    )
    db_session.add(variant)
    await db_session.flush()

    fetched = await repo.get_by_id(variant.id)
    assert fetched is not None
    assert fetched.name == "Variant"

    variants = await repo.get_by_product(product.id)
    assert len(variants) == 1

    await repo.delete(variant.id)
    assert await repo.get_by_id(variant.id) is None


@pytest.mark.asyncio
async def test_product_variant_repository_duplicate_sku(db_session: AsyncSession):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    product = Product(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-1",
        price=10.00,
    )
    db_session.add(product)
    await db_session.flush()

    repo = ProductVariantRepository(db_session)
    variant = ProductVariant(
        product_id=product.id,
        name="Variant",
        sku="VAR-001",
        price=15.00,
    )
    db_session.add(variant)
    await db_session.flush()

    assert await repo.exists_by_sku("VAR-001") is True
    assert await repo.exists_by_sku_excluding_id("VAR-001", variant.id) is False
    assert await repo.exists_by_sku_excluding_id("VAR-001", uuid.uuid4()) is True
