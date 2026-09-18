import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient

from app.modules.product.models import Brand, Category, Product


async def _create_product(db_session) -> Product:
    brand = Brand(
        name="Test Brand",
        slug="test-brand",
        description="A test brand",
    )
    category = Category(
        name="Test Category",
        slug="test-category",
        description="A test category",
    )
    db_session.add_all([brand, category])
    await db_session.flush()

    product = Product(
        brand_id=brand.id,
        category_id=category.id,
        name="Test Product",
        slug="test-product",
        sku="SKU-10",
        price=Decimal("10.00"),
        stock_quantity=100,
        is_active=True,
    )
    db_session.add(product)
    await db_session.flush()
    return product


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, db_session):
    product = await _create_product(db_session)

    payload = {
        "customer_id": str(uuid.uuid4()),
        "items": [
            {"product_id": str(product.id), "quantity": 2},
        ],
        "currency": "USD",
        "status": "pending",
    }
    response = await client.post("/api/v1/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["order_number"].startswith("ORD-")
    assert data["status"] == "pending"
    assert data["total_amount"] == "20.00"


@pytest.mark.asyncio
async def test_get_order_not_found(client: AsyncClient):
    response = await client.get(f"/api/v1/orders/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_orders(client: AsyncClient, db_session):
    product = await _create_product(db_session)

    payload = {
        "customer_id": str(uuid.uuid4()),
        "items": [
            {"product_id": str(product.id), "quantity": 1},
        ],
        "currency": "USD",
        "status": "pending",
    }
    await client.post("/api/v1/orders", json=payload)

    response = await client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_create_order_item(client: AsyncClient, db_session):
    product = await _create_product(db_session)

    order_payload = {
        "customer_id": str(uuid.uuid4()),
        "items": [
            {"product_id": str(product.id), "quantity": 1},
        ],
        "currency": "USD",
        "status": "pending",
    }
    order_response = await client.post("/api/v1/orders", json=order_payload)
    assert order_response.status_code == 201
    order_id = order_response.json()["id"]

    item_payload = {
        "product_id": str(product.id),
        "quantity": 3,
    }
    response = await client.post(f"/api/v1/orders/{order_id}/items", json=item_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 3
    assert data["product_id"] == str(product.id)


@pytest.mark.asyncio
async def test_create_shipping_address(client: AsyncClient, db_session):
    product = await _create_product(db_session)

    order_payload = {
        "customer_id": str(uuid.uuid4()),
        "items": [
            {"product_id": str(product.id), "quantity": 1},
        ],
        "currency": "USD",
        "status": "pending",
    }
    order_response = await client.post("/api/v1/orders", json=order_payload)
    assert order_response.status_code == 201
    order_id = order_response.json()["id"]

    address_payload = {
        "full_name": "John Doe",
        "phone": "1234567890",
        "address_line1": "123 Main St",
        "city": "City",
        "state": "State",
        "postal_code": "12345",
        "country": "US",
    }
    response = await client.post(
        f"/api/v1/orders/{order_id}/shipping-address",
        json=address_payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"


@pytest.mark.asyncio
async def test_create_billing_address(client: AsyncClient, db_session):
    product = await _create_product(db_session)

    order_payload = {
        "customer_id": str(uuid.uuid4()),
        "items": [
            {"product_id": str(product.id), "quantity": 1},
        ],
        "currency": "USD",
        "status": "pending",
    }
    order_response = await client.post("/api/v1/orders", json=order_payload)
    assert order_response.status_code == 201
    order_id = order_response.json()["id"]

    address_payload = {
        "full_name": "John Doe",
        "phone": "1234567890",
        "address_line1": "123 Main St",
        "city": "City",
        "state": "State",
        "postal_code": "12345",
        "country": "US",
    }
    response = await client.post(
        f"/api/v1/orders/{order_id}/billing-address",
        json=address_payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"
