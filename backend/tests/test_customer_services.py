import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customer.services.customer import CustomerService


@pytest.mark.asyncio
async def test_customer_service_create(db_session: AsyncSession):
    service = CustomerService(db_session)
    customer = await service.create(
        full_name="John Doe",
        email="john@example.com",
        phone="+8801234567890",
        status="active",
        skin_type="oily",
        skin_concerns=["acne", "dryness"],
    )
    assert customer.id is not None
    assert customer.email == "john@example.com"
    assert customer.status == "active"


@pytest.mark.asyncio
async def test_customer_service_create_duplicate_email(db_session: AsyncSession):
    service = CustomerService(db_session)
    await service.create(
        full_name="John Doe",
        email="john@example.com",
        status="active",
    )

    with pytest.raises(ValueError, match="Email john@example.com is already in use"):
        await service.create(
            full_name="Jane Doe",
            email="john@example.com",
            status="active",
        )


@pytest.mark.asyncio
async def test_customer_service_create_duplicate_phone(db_session: AsyncSession):
    service = CustomerService(db_session)
    await service.create(
        full_name="John Doe",
        email="john@example.com",
        phone="+8801234567890",
        status="active",
    )

    with pytest.raises(ValueError, match=r"Phone \+8801234567890 is already in use"):
        await service.create(
            full_name="Jane Doe",
            email="jane@example.com",
            phone="+8801234567890",
            status="active",
        )


@pytest.mark.asyncio
async def test_customer_service_create_invalid_status(db_session: AsyncSession):
    service = CustomerService(db_session)
    with pytest.raises(ValueError, match="Invalid status"):
        await service.create(
            full_name="John Doe",
            email="john@example.com",
            status="invalid",
        )


@pytest.mark.asyncio
async def test_customer_service_update(db_session: AsyncSession):
    service = CustomerService(db_session)
    customer = await service.create(
        full_name="John Doe",
        email="john@example.com",
        status="active",
    )

    updated = await service.update(
        customer_id=customer.id,
        full_name="Jane Doe",
        status="inactive",
    )
    assert updated.full_name == "Jane Doe"
    assert updated.status == "inactive"


@pytest.mark.asyncio
async def test_customer_service_update_not_found(db_session: AsyncSession):
    service = CustomerService(db_session)
    with pytest.raises(ValueError, match="Customer not found"):
        await service.update(
            customer_id=uuid.uuid4(),
            full_name="Jane Doe",
        )


@pytest.mark.asyncio
async def test_customer_service_update_email_normalization(db_session: AsyncSession):
    service = CustomerService(db_session)
    customer = await service.create(
        full_name="John Doe",
        email="john@example.com",
        status="active",
    )

    updated = await service.update(
        customer_id=customer.id,
        email="  JANE@EXAMPLE.COM  ",
    )
    assert updated.email == "jane@example.com"


@pytest.mark.asyncio
async def test_customer_service_delete(db_session: AsyncSession):
    service = CustomerService(db_session)
    customer = await service.create(
        full_name="John Doe",
        email="john@example.com",
        status="active",
    )

    await service.delete(customer.id)
    assert await service.get_by_id(customer.id) is None


@pytest.mark.asyncio
async def test_customer_service_delete_not_found(db_session: AsyncSession):
    service = CustomerService(db_session)
    with pytest.raises(ValueError, match="Customer not found"):
        await service.delete(uuid.uuid4())


@pytest.mark.asyncio
async def test_customer_service_get_list(db_session: AsyncSession):
    service = CustomerService(db_session)
    await service.create(full_name="Active 1", email="a1@example.com", status="active")
    await service.create(full_name="Active 2", email="a2@example.com", status="active")
    await service.create(full_name="Inactive", email="i@example.com", status="inactive")

    active_customers, total = await service.get_list(status="active")
    assert len(active_customers) == 2
    assert total == 2

    all_customers, total = await service.get_list(search="Active 1")
    assert len(all_customers) >= 1
    assert total >= 1
