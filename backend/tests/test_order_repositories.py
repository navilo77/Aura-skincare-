import uuid
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import BillingAddress, Order, OrderItem, ShippingAddress
from app.modules.order.repositories.billing_address import BillingAddressRepository
from app.modules.order.repositories.order import OrderRepository
from app.modules.order.repositories.order_item import OrderItemRepository
from app.modules.order.repositories.shipping_address import ShippingAddressRepository


@pytest.mark.asyncio
async def test_order_repository_crud(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    order = Order(
        customer_id=uuid.uuid4(),
        order_number="ORD-001",
        status="pending",
        total_amount=Decimal("100.00"),
        currency="USD",
    )
    db_session.add(order)
    await db_session.flush()

    fetched = await repo.get_by_id(order.id)
    assert fetched is not None
    assert fetched.order_number == "ORD-001"

    order.status = "processing"
    updated = await repo.update(order)
    assert updated.status == "processing"

    assert await repo.get_by_order_number("ORD-001") is not None

    await repo.delete(order.id)
    assert await repo.get_by_id(order.id) is None


@pytest.mark.asyncio
async def test_order_repository_filters(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    customer_id = uuid.uuid4()
    order = Order(
        customer_id=customer_id,
        order_number="ORD-002",
        status="pending",
        total_amount=Decimal("50.00"),
        currency="USD",
    )
    db_session.add(order)
    await db_session.flush()

    by_customer = await repo.get_by_customer(customer_id)
    assert len(by_customer[0]) == 1

    by_status = await repo.get_by_status("pending")
    assert len(by_status[0]) == 1

    orders, total = await repo.get_list(customer_id=customer_id, status="pending")
    assert total == 1


@pytest.mark.asyncio
async def test_order_item_repository_crud(db_session: AsyncSession):
    order = Order(
        customer_id=uuid.uuid4(),
        order_number="ORD-003",
        status="pending",
        total_amount=Decimal("0.00"),
        currency="USD",
    )
    db_session.add(order)
    await db_session.flush()

    repo = OrderItemRepository(db_session)
    item = OrderItem(
        order_id=order.id,
        product_id=uuid.uuid4(),
        quantity=2,
        unit_price=Decimal("10.00"),
        total_price=Decimal("20.00"),
        product_name="Product",
        sku="SKU-1",
    )
    db_session.add(item)
    await db_session.flush()

    fetched = await repo.get_by_id(item.id)
    assert fetched is not None
    assert fetched.product_name == "Product"

    items, total = await repo.get_items_by_order(order.id)
    assert len(items) == 1

    await repo.delete(item.id)
    assert await repo.get_by_id(item.id) is None


@pytest.mark.asyncio
async def test_shipping_address_repository_crud(db_session: AsyncSession):
    order = Order(
        customer_id=uuid.uuid4(),
        order_number="ORD-004",
        status="pending",
        total_amount=Decimal("0.00"),
        currency="USD",
    )
    db_session.add(order)
    await db_session.flush()

    repo = ShippingAddressRepository(db_session)
    address = ShippingAddress(
        order_id=order.id,
        full_name="John Doe",
        phone="1234567890",
        address_line1="123 Main St",
        city="City",
        state="State",
        postal_code="12345",
        country="US",
    )
    db_session.add(address)
    await db_session.flush()

    fetched = await repo.get_by_id(address.id)
    assert fetched is not None
    assert fetched.full_name == "John Doe"

    shipping = await repo.get_shipping_address(order.id)
    assert shipping is not None

    await repo.delete(address.id)
    assert await repo.get_by_id(address.id) is None


@pytest.mark.asyncio
async def test_billing_address_repository_crud(db_session: AsyncSession):
    order = Order(
        customer_id=uuid.uuid4(),
        order_number="ORD-005",
        status="pending",
        total_amount=Decimal("0.00"),
        currency="USD",
    )
    db_session.add(order)
    await db_session.flush()

    repo = BillingAddressRepository(db_session)
    address = BillingAddress(
        order_id=order.id,
        full_name="John Doe",
        phone="1234567890",
        address_line1="123 Main St",
        city="City",
        state="State",
        postal_code="12345",
        country="US",
    )
    db_session.add(address)
    await db_session.flush()

    fetched = await repo.get_by_id(address.id)
    assert fetched is not None
    assert fetched.full_name == "John Doe"

    billing = await repo.get_billing_address(order.id)
    assert billing is not None

    await repo.delete(address.id)
    assert await repo.get_by_id(address.id) is None
