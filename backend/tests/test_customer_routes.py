import uuid

import pytest
from httpx import AsyncClient

from app.modules.customer.models import Customer


async def _create_customer(db_session) -> Customer:
    customer = Customer(
        full_name="Test Customer",
        email="test@example.com",
        phone="+8801234567890",
        status="active",
        skin_type="oily",
        skin_concerns=["acne", "dryness"],
    )
    db_session.add(customer)
    await db_session.flush()
    return customer


@pytest.mark.asyncio
async def test_create_customer(client: AsyncClient):
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+8801234567890",
        "status": "active",
        "skin_type": "oily",
        "skin_concerns": ["acne", "dryness"],
    }
    response = await client.post("/api/v1/customers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_get_customer_not_found(client: AsyncClient):
    response = await client.get(f"/api/v1/customers/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_customers(client: AsyncClient, db_session):
    await _create_customer(db_session)

    response = await client.get("/api/v1/customers")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_update_customer(client: AsyncClient, db_session):
    customer = await _create_customer(db_session)

    payload = {"full_name": "Jane Doe", "status": "inactive"}
    response = await client.patch(
        f"/api/v1/customers/{customer.id}", json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["status"] == "inactive"


@pytest.mark.asyncio
async def test_delete_customer(client: AsyncClient, db_session):
    customer = await _create_customer(db_session)

    response = await client.delete(f"/api/v1/customers/{customer.id}")
    assert response.status_code == 204

    get_response = await client.get(f"/api/v1/customers/{customer.id}")
    assert get_response.status_code == 404
