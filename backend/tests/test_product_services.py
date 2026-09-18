import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.services.brand import BrandService
from app.modules.product.services.category import CategoryService
from app.modules.product.services.product import ProductService
from app.modules.product.services.product_image import ProductImageService
from app.modules.product.services.product_variant import ProductVariantService


@pytest.mark.asyncio
async def test_brand_service_crud(db_session: AsyncSession):
    service = BrandService(db_session)
    brand = await service.create(
        name="Test Brand",
        slug="test-brand",
        description="A test brand",
    )
    assert brand.id is not None
    assert brand.name == "Test Brand"

    fetched = await service.get_by_id(brand.id)
    assert fetched is not None

    brands, total = await service.get_list()
    assert total == 1

    updated = await service.update(brand_id=brand.id, name="Updated Brand")
    assert updated.name == "Updated Brand"

    await service.delete(brand.id)
    assert await service.get_by_id(brand.id) is None


@pytest.mark.asyncio
async def test_brand_service_duplicate_slug(db_session: AsyncSession):
    service = BrandService(db_session)
    await service.create(name="Brand A", slug="brand-a")

    with pytest.raises(ValueError) as exc:
        await service.create(name="Brand B", slug="brand-a")
    assert "slug already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_category_service_crud(db_session: AsyncSession):
    service = CategoryService(db_session)
    category = await service.create(name="Test Category", slug="test-category")
    assert category.id is not None
    assert category.name == "Test Category"

    fetched = await service.get_by_id(category.id)
    assert fetched is not None

    updated = await service.update(category_id=category.id, name="Updated Category")
    assert updated.name == "Updated Category"

    await service.delete(category.id)
    assert await service.get_by_id(category.id) is None


@pytest.mark.asyncio
async def test_category_service_parent_validation(db_session: AsyncSession):
    service = CategoryService(db_session)
    parent = await service.create(name="Parent", slug="parent")
    child = await service.create(name="Child", slug="child", parent_id=parent.id)
    assert child.parent_id == parent.id

    with pytest.raises(ValueError) as exc:
        await service.create(name="Orphan", slug="orphan", parent_id=uuid.uuid4())
    assert "Parent category not found" in str(exc.value)

    with pytest.raises(ValueError) as exc:
        await service.update(category_id=child.id, parent_id=child.id)
    assert "cannot be its own parent" in str(exc.value)


@pytest.mark.asyncio
async def test_category_service_cannot_delete_with_children(db_session: AsyncSession):
    service = CategoryService(db_session)
    parent = await service.create(name="Parent", slug="parent")
    await service.create(name="Child", slug="child", parent_id=parent.id)

    with pytest.raises(ValueError) as exc:
        await service.delete(parent.id)
    assert "Cannot delete category with child categories" in str(exc.value)


@pytest.mark.asyncio
async def test_product_service_crud(db_session: AsyncSession):
    brand_service = BrandService(db_session)
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)

    brand = await brand_service.create(name="Brand", slug="brand")
    category = await category_service.create(name="Category", slug="category")

    product = await product_service.create(
        brand_id=brand.id,
        category_id=category.id,
        name="Test Product",
        slug="test-product",
        sku="SKU-001",
        price=10.00,
        currency="USD",
    )
    assert product.id is not None
    assert product.name == "Test Product"

    fetched = await product_service.get_by_id(product.id)
    assert fetched is not None

    products, total = await product_service.get_list()
    assert total == 1

    updated = await product_service.update(
        product_id=product.id, name="Updated Product"
    )
    assert updated.name == "Updated Product"

    await product_service.delete(product.id)
    assert await product_service.get_by_id(product.id) is None


@pytest.mark.asyncio
async def test_product_service_duplicate_slug_and_sku(db_session: AsyncSession):
    brand_service = BrandService(db_session)
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)

    brand = await brand_service.create(name="Brand", slug="brand")
    category = await category_service.create(name="Category", slug="category")

    await product_service.create(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-001",
        price=10.00,
        currency="USD",
    )

    with pytest.raises(ValueError) as exc:
        await product_service.create(
            brand_id=brand.id,
            category_id=category.id,
            name="Product 2",
            slug="product",
            sku="SKU-002",
            price=20.00,
            currency="USD",
        )
    assert "slug already exists" in str(exc.value)

    with pytest.raises(ValueError) as exc:
        await product_service.create(
            brand_id=brand.id,
            category_id=category.id,
            name="Product 2",
            slug="product-2",
            sku="SKU-001",
            price=20.00,
            currency="USD",
        )
    assert "SKU already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_product_service_invalid_brand_and_category(db_session: AsyncSession):
    product_service = ProductService(db_session)

    with pytest.raises(ValueError) as exc:
        await product_service.create(
            brand_id=uuid.uuid4(),
            category_id=uuid.uuid4(),
            name="Product",
            slug="product",
            sku="SKU-001",
            price=10.00,
            currency="USD",
        )
    assert "Brand not found" in str(exc.value)


@pytest.mark.asyncio
async def test_product_image_service_crud(db_session: AsyncSession):
    brand_service = BrandService(db_session)
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)
    image_service = ProductImageService(db_session)

    brand = await brand_service.create(name="Brand", slug="brand")
    category = await category_service.create(name="Category", slug="category")
    product = await product_service.create(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-001",
        price=10.00,
        currency="USD",
    )

    image = await image_service.create(
        product_id=product.id,
        image_url="http://example.com/img.jpg",
    )
    assert image.id is not None

    fetched = await image_service.get_by_id(image.id)
    assert fetched is not None

    images = await image_service.get_by_product(product.id)
    assert len(images) == 1

    await image_service.delete(image.id)
    assert await image_service.get_by_id(image.id) is None


@pytest.mark.asyncio
async def test_product_image_service_invalid_product(db_session: AsyncSession):
    image_service = ProductImageService(db_session)

    with pytest.raises(ValueError) as exc:
        await image_service.create(
            product_id=uuid.uuid4(),
            image_url="http://example.com/img.jpg",
        )
    assert "Product not found" in str(exc.value)


@pytest.mark.asyncio
async def test_product_variant_service_crud(db_session: AsyncSession):
    brand_service = BrandService(db_session)
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)
    variant_service = ProductVariantService(db_session)

    brand = await brand_service.create(name="Brand", slug="brand")
    category = await category_service.create(name="Category", slug="category")
    product = await product_service.create(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-001",
        price=10.00,
        currency="USD",
    )

    variant = await variant_service.create(
        product_id=product.id,
        name="Variant",
        sku="VAR-001",
        price=15.00,
    )
    assert variant.id is not None

    fetched = await variant_service.get_by_id(variant.id)
    assert fetched is not None

    variants = await variant_service.get_by_product(product.id)
    assert len(variants) == 1

    await variant_service.delete(variant.id)
    assert await variant_service.get_by_id(variant.id) is None


@pytest.mark.asyncio
async def test_product_variant_service_duplicate_sku(db_session: AsyncSession):
    brand_service = BrandService(db_session)
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)
    variant_service = ProductVariantService(db_session)

    brand = await brand_service.create(name="Brand", slug="brand")
    category = await category_service.create(name="Category", slug="category")
    product = await product_service.create(
        brand_id=brand.id,
        category_id=category.id,
        name="Product",
        slug="product",
        sku="SKU-001",
        price=10.00,
        currency="USD",
    )

    await variant_service.create(
        product_id=product.id,
        name="Variant",
        sku="VAR-001",
        price=15.00,
    )

    with pytest.raises(ValueError) as exc:
        await variant_service.create(
            product_id=product.id,
            name="Variant 2",
            sku="VAR-001",
            price=20.00,
        )
    assert "SKU already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_product_service_pagination_and_search(db_session: AsyncSession):
    brand_service = BrandService(db_session)
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)

    brand = await brand_service.create(name="Brand", slug="brand")
    category = await category_service.create(name="Category", slug="category")

    for i in range(5):
        await product_service.create(
            brand_id=brand.id,
            category_id=category.id,
            name=f"Product {i}",
            slug=f"product-{i}",
            sku=f"SKU-{i}",
            price=10.00 + i,
            currency="USD",
        )

    products, total = await product_service.get_list(skip=0, limit=2)
    assert len(products) == 2
    assert total == 5

    products, total = await product_service.get_list(search="Product 1")
    assert total == 1
    assert products[0].name == "Product 1"

    products, total = await product_service.get_list(brand_id=brand.id)
    assert total == 5

    products, total = await product_service.get_list(category_id=category.id)
    assert total == 5
