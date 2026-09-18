import uuid
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.services.order import OrderService
from app.modules.product.models import Brand, Category, Product


async def _create_product(db_session: AsyncSession) -> Product:
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
        sku="SKU-1",
        price=Decimal("10.00"),
        stock_quantity=100,
        is_active=True,
    )
    db_session.add(product)
    await db_session.flush()
    return product


@pytest.mark.asyncio
async def test_order_service_create(db_session: AsyncSession):
    product = await _create_product(db_session)

    service = OrderService(db_session)
    order = await service.create(
        customer_id=uuid.uuid4(),
        items=[
            {"product_id": product.id, "quantity": 2},
        ],
        currency="USD",
    )
    assert order.id is not None
    assert order.status == "pending"
    assert order.order_number.startswith("ORD-")


@pytest.mark.asyncio
async def test_order_service_create_requires_items(db_session: AsyncSession):
    service = OrderService(db_session)
    with pytest.raises(ValueError, match="Order must have at least one item"):
        await service.create(
            customer_id=uuid.uuid4(),
            items=[],
            currency="USD",
        )


@pytest.mark.asyncio
async def test_order_service_create_invalid_product(db_session: AsyncSession):
    service = OrderService(db_session)
    with pytest.raises(ValueError, match="Product .* not found"):
        await service.create(
            customer_id=uuid.uuid4(),
            items=[
                {"product_id": uuid.uuid4(), "quantity": 1},
            ],
            currency="USD",
        )


@pytest.mark.asyncio
async def test_order_service_update_status(db_session: AsyncSession):
    product = await _create_product(db_session)

    service = OrderService(db_session)
    order = await service.create(
        customer_id=uuid.uuid4(),
        items=[
            {"product_id": product.id, "quantity": 1},
        ],
        currency="USD",
    )
    assert order.status == "pending"

    updated = await service.update(order.id, status="processing")
    assert updated.status == "processing"


@pytest.mark.asyncio
async def test_order_service_invalid_status_transition(db_session: AsyncSession):
    product = await _create_product(db_session)

    service = OrderService(db_session)
    order = await service.create(
        customer_id=uuid.uuid4(),
        items=[
            {"product_id": product.id, "quantity": 1},
        ],
        currency="USD",
    )
    assert order.status == "pending"

    with pytest.raises(ValueError, match="Cannot transition"):
        await service.update(order.id, status="delivered")


@pytest.mark.asyncio
async def test_order_service_delete_completed(db_session: AsyncSession):
    product = await _create_product(db_session)

    service = OrderService(db_session)
    order = await service.create(
        customer_id=uuid.uuid4(),
        items=[
            {"product_id": product.id, "quantity": 1},
        ],
        currency="USD",
    )
    await service.update(order.id, status="processing")
    await service.update(order.id, status="shipped")
    updated = await service.update(order.id, status="delivered")
    assert updated.status == "delivered"

    with pytest.raises(ValueError, match="Cannot delete completed orders"):
        await service.delete(order.id)
