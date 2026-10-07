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


async def _register_and_login(
    client: AsyncClient, email: str, role: str = "admin"
) -> str:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "secure123",
            "full_name": "Test User",
            "role": role,
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "secure123",
        },
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_customer(client: AsyncClient):
    token = await _register_and_login(
        client, "customer-admin@example.com", role="admin"
    )
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+8801234567890",
        "status": "active",
        "skin_type": "oily",
        "skin_concerns": ["acne", "dryness"],
    }
    response = await client.post(
        "/api/v1/customers", json=payload, headers=_auth_headers(token)
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_get_customer_not_found(client: AsyncClient):
    token = await _register_and_login(client, "customer-get@example.com", role="admin")
    response = await client.get(
        f"/api/v1/customers/{uuid.uuid4()}", headers=_auth_headers(token)
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_customers(client: AsyncClient, db_session):
    await _create_customer(db_session)
    token = await _register_and_login(client, "customer-list@example.com", role="admin")
    response = await client.get("/api/v1/customers", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_update_customer(client: AsyncClient, db_session):
    customer = await _create_customer(db_session)
    token = await _register_and_login(
        client, "customer-update@example.com", role="admin"
    )
    payload = {"full_name": "Jane Doe", "status": "inactive"}
    response = await client.patch(
        f"/api/v1/customers/{customer.id}", json=payload, headers=_auth_headers(token)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["status"] == "inactive"


@pytest.mark.asyncio
async def test_delete_customer(client: AsyncClient, db_session):
    customer = await _create_customer(db_session)
    token = await _register_and_login(
        client, "customer-delete@example.com", role="admin"
    )
    response = await client.delete(
        f"/api/v1/customers/{customer.id}", headers=_auth_headers(token)
    )
    assert response.status_code == 204

    get_response = await client.get(
        f"/api/v1/customers/{customer.id}", headers=_auth_headers(token)
    )
    assert get_response.status_code == 404
