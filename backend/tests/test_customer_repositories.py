
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customer.models import Customer
from app.modules.customer.repositories.customer import CustomerRepository


@pytest.mark.asyncio
async def test_customer_repository_crud(db_session: AsyncSession):
    repo = CustomerRepository(db_session)
    customer = Customer(
        full_name="Test Customer",
        email="test@example.com",
        phone="+8801234567890",
        status="active",
        skin_type="oily",
        skin_concerns=["acne"],
    )
    db_session.add(customer)
    await db_session.flush()

    fetched = await repo.get_by_id(customer.id)
    assert fetched is not None
    assert fetched.full_name == "Test Customer"

    customer.status = "inactive"
    updated = await repo.update(customer)
    assert updated.status == "inactive"

    assert await repo.get_by_email("test@example.com") is not None
    assert await repo.get_by_phone("+8801234567890") is not None

    await repo.delete(customer.id)
    assert await repo.get_by_id(customer.id) is None


@pytest.mark.asyncio
async def test_customer_repository_exists_checks(db_session: AsyncSession):
    repo = CustomerRepository(db_session)
    customer = Customer(
        full_name="Exists Check",
        email="exists@example.com",
        phone="+8801111111111",
        status="active",
    )
    db_session.add(customer)
    await db_session.flush()

    assert await repo.exists_by_email("exists@example.com") is True
    assert await repo.exists_by_email("missing@example.com") is False
    assert await repo.exists_by_phone("+8801111111111") is True
    assert await repo.exists_by_phone("+8800000000000") is False
    assert await repo.exists_by_email_excluding_id(
        "exists@example.com", customer.id
    ) is False
    assert await repo.exists_by_phone_excluding_id(
        "+8801111111111", customer.id
    ) is False


@pytest.mark.asyncio
async def test_customer_repository_get_list(db_session: AsyncSession):
    repo = CustomerRepository(db_session)
    for i in range(3):
        customer = Customer(
            full_name=f"Customer {i}",
            email=f"customer{i}@example.com",
            status="active" if i < 2 else "inactive",
        )
        db_session.add(customer)
    await db_session.flush()

    active_customers, total = await repo.get_list(status="active")
    assert len(active_customers) == 2
    assert total == 2

    all_customers, total = await repo.get_list(search="Customer")
    assert total == 3
