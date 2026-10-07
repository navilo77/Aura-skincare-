import uuid

import pytest
from fastapi import status
from httpx import AsyncClient

from app.modules.product.models import (
    Brand,
    Category,
)


def _brand_payload(name="Test Brand", slug="test-brand"):
    return {"name": name, "slug": slug, "description": "A test brand", "logo_url": None}


def _category_payload(name="Test Category", slug="test-category", parent_id=None):
    return {
        "name": name,
        "slug": slug,
        "parent_id": parent_id,
        "description": None,
        "image_url": None,
        "sort_order": 0,
    }


def _product_payload(
    brand_id,
    category_id,
    name="Test Product",
    slug="test-product",
    sku="SKU-001",
):
    return {
        "brand_id": str(brand_id),
        "category_id": str(category_id),
        "name": name,
        "slug": slug,
        "sku": sku,
        "short_description": None,
        "description": None,
        "status": "draft",
        "product_type": "simple",
        "price": 10.00,
        "compare_at_price": None,
        "currency": "USD",
        "stock_quantity": 0,
        "thumbnail_url": None,
        "is_featured": False,
        "is_active": True,
    }


def _image_payload(image_url="http://example.com/img.jpg"):
    return {
        "image_url": image_url,
        "alt_text": None,
        "sort_order": 0,
        "is_primary": False,
    }


def _variant_payload(name="Variant", sku="VAR-001", price=15.00):
    return {
        "name": name,
        "sku": sku,
        "price": price,
        "stock_quantity": 0,
        "attributes": None,
        "is_active": True,
    }


@pytest.mark.asyncio
async def test_brand_route_crud(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    db_session.add(brand)
    await db_session.flush()

    response = await client.get("/api/v1/products/brands")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1

    response = await client.get(f"/api/v1/products/brands/{brand.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Brand"

    response = await client.post("/api/v1/products/brands", json=_brand_payload())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test Brand"

    response = await client.patch(
        f"/api/v1/products/brands/{brand.id}",
        json={"name": "Updated"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated"

    response = await client.delete(f"/api/v1/products/brands/{brand.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_brand_route_duplicate_slug(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    db_session.add(brand)
    await db_session.flush()

    response = await client.post(
        "/api/v1/products/brands",
        json=_brand_payload(slug="brand"),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_category_route_crud(client: AsyncClient, db_session):
    category = Category(name="Category", slug="category")
    db_session.add(category)
    await db_session.flush()

    response = await client.get("/api/v1/products/categories")
    assert response.status_code == status.HTTP_200_OK

    response = await client.get(f"/api/v1/products/categories/{category.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Category"

    response = await client.post(
        "/api/v1/products/categories",
        json=_category_payload(),
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test Category"

    response = await client.patch(
        f"/api/v1/products/categories/{category.id}",
        json={"name": "Updated"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated"

    response = await client.delete(f"/api/v1/products/categories/{category.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_category_route_parent_validation(client: AsyncClient, db_session):
    parent = Category(name="Parent", slug="parent")
    db_session.add(parent)
    await db_session.flush()

    response = await client.post(
        "/api/v1/products/categories",
        json=_category_payload(name="Child", slug="child", parent_id=str(parent.id)),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(
        "/api/v1/products/categories",
        json=_category_payload(
            name="Orphan",
            slug="orphan",
            parent_id=str(uuid.uuid4()),
        ),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_category_route_cannot_delete_with_children(
    client: AsyncClient,
    db_session,
):
    parent = Category(name="Parent", slug="parent")
    db_session.add(parent)
    await db_session.flush()

    child = Category(name="Child", slug="child", parent_id=parent.id)
    db_session.add(child)
    await db_session.flush()

    response = await client.delete(f"/api/v1/products/categories/{parent.id}")
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_category_tree_route(client: AsyncClient, db_session):
    parent = Category(name="Parent", slug="parent")
    db_session.add(parent)
    await db_session.flush()

    child = Category(name="Child", slug="child", parent_id=parent.id)
    db_session.add(child)
    await db_session.flush()

    response = await client.get("/api/v1/products/categories/tree")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Parent"
    assert len(data[0]["children"]) == 1


@pytest.mark.asyncio
async def test_product_route_crud(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id),
    )
    assert response.status_code == status.HTTP_201_CREATED
    product_id = response.json()["id"]

    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test Product"

    response = await client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK

    response = await client.patch(
        f"/api/v1/products/{product_id}",
        json={"name": "Updated Product"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Product"

    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_product_route_duplicate_slug_and_sku(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, slug="product", sku="SKU-001"),
    )

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, slug="product", sku="SKU-002"),
    )
    assert response.status_code == status.HTTP_409_CONFLICT

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, slug="product-2", sku="SKU-001"),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_product_route_pagination_and_filtering(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    for i in range(5):
        await client.post(
            "/api/v1/products",
            json=_product_payload(
                brand.id,
                category.id,
                name=f"Product {i}",
                slug=f"product-{i}",
                sku=f"SKU-{i}",
            ),
        )

    response = await client.get("/api/v1/products?page=1&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

    response = await client.get("/api/v1/products?search=Product 1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1

    response = await client.get(f"/api/v1/products?brand_slug={brand.slug}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 5


@pytest.mark.asyncio
async def test_product_image_route_crud(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    product_response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id),
    )
    product_id = product_response.json()["id"]

    response = await client.post(
        f"/api/v1/products/images/{product_id}",
        json=_image_payload(),
    )
    assert response.status_code == status.HTTP_201_CREATED
    image_id = response.json()["id"]

    response = await client.get(f"/api/v1/products/images/{image_id}")
    assert response.status_code == status.HTTP_200_OK

    response = await client.get(f"/api/v1/products/images?product_id={product_id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    response = await client.patch(
        f"/api/v1/products/images/{image_id}",
        json={"alt_text": "Updated"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["alt_text"] == "Updated"

    response = await client.delete(f"/api/v1/products/images/{image_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_product_image_route_invalid_product(client: AsyncClient, db_session):
    response = await client.post(
        f"/api/v1/products/images/{uuid.uuid4()}",
        json=_image_payload(),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_product_variant_route_crud(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    product_response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id),
    )
    product_id = product_response.json()["id"]

    response = await client.post(
        f"/api/v1/products/variants/{product_id}",
        json=_variant_payload(),
    )
    assert response.status_code == status.HTTP_201_CREATED
    variant_id = response.json()["id"]

    response = await client.get(f"/api/v1/products/variants/{variant_id}")
    assert response.status_code == status.HTTP_200_OK

    response = await client.get(f"/api/v1/products/variants?product_id={product_id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    response = await client.patch(
        f"/api/v1/products/variants/{variant_id}",
        json={"name": "Updated Variant"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Variant"

    response = await client.delete(f"/api/v1/products/variants/{variant_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_product_variant_route_duplicate_sku(client: AsyncClient, db_session):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    product_response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id),
    )
    product_id = product_response.json()["id"]

    await client.post(
        f"/api/v1/products/variants/{product_id}",
        json=_variant_payload(sku="VAR-001"),
    )

    response = await client.post(
        f"/api/v1/products/variants/{product_id}",
        json=_variant_payload(name="Variant 2", sku="VAR-001"),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_product_route_not_found(client: AsyncClient, db_session):
    response = await client.get(f"/api/v1/products/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await client.delete(f"/api/v1/products/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_product_route_valid_brand_slug_returns_products(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(f"/api/v1/products?brand_slug={brand.slug}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_product_route_invalid_brand_slug_returns_empty(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get("/api/v1/products?brand_slug=invalid-brand")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_product_route_valid_category_slug_returns_products(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(f"/api/v1/products?category_slug={category.slug}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_product_route_invalid_category_slug_returns_empty(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get("/api/v1/products?category_slug=invalid-category")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_product_route_existing_brand_invalid_category_returns_empty(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(
        f"/api/v1/products?brand_slug={brand.slug}&category_slug=invalid-category"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_product_route_invalid_brand_existing_category_returns_empty(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(
        f"/api/v1/products?brand_slug=invalid-brand&category_slug={category.slug}"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_product_route_invalid_brand_invalid_category_returns_empty(
    client: AsyncClient, db_session
):
    brand = Brand(name="Brand", slug="brand")
    category = Category(name="Category", slug="category")
    db_session.add_all([brand, category])
    await db_session.flush()

    response = await client.post(
        "/api/v1/products",
        json=_product_payload(brand.id, category.id, name="Product A"),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(
        "/api/v1/products?brand_slug=invalid-brand&category_slug=invalid-category"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
