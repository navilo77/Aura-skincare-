import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    payload = {
        "email": "test@example.com",
        "password": "StrongPass1!",
        "full_name": "Test User",
        "role": "customer",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert "id" in data


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    register_payload = {
        "email": "login@example.com",
        "password": "StrongPass1!",
        "full_name": "Login User",
        "role": "customer",
    }
    await client.post("/api/v1/auth/register", json=register_payload)

    login_payload = {
        "email": "login@example.com",
        "password": "StrongPass1!",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    register_payload = {
        "email": "badpass@example.com",
        "password": "StrongPass1!",
        "full_name": "Bad Password",
        "role": "customer",
    }
    await client.post("/api/v1/auth/register", json=register_payload)

    login_payload = {
        "email": "badpass@example.com",
        "password": "WrongPassword",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, db_session):
    from app.modules.auth.models import User
    from app.shared.security.password import hash_password

    user = User(
        email="inactive@example.com",
        password_hash=hash_password("StrongPass1!"),
        full_name="Inactive User",
        role="customer",
        is_active=False,
    )
    db_session.add(user)
    await db_session.flush()

    login_payload = {
        "email": "inactive@example.com",
        "password": "StrongPass1!",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
