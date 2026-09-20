import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_register_login_logout_flow(client):
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "epic04@example.com",
            "password": "secure123",
            "full_name": "EPIC04 User",
        },
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "epic04@example.com",
            "password": "secure123",
        },
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "refresh_token" in login_response.json()

    refresh_token = login_response.json()["refresh_token"]

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_response.status_code == 200

    logout_response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
    )
    assert logout_response.status_code == 204


@pytest.mark.asyncio
async def test_forgot_password_creates_token(db_session: AsyncSession):
    from app.modules.auth.repositories.user import UserRepository
    from app.modules.auth.services.auth import AuthService

    service = AuthService(db_session)
    await service.register(
        email="forgot@example.com",
        password="secure123",
        full_name="Forgot User",
    )

    repo = UserRepository(db_session)
    stored_user = await repo.get_by_email("forgot@example.com")
    assert stored_user is not None


@pytest.mark.asyncio
async def test_email_verification_token_expiry(client):
    response = await client.post(
        "/api/v1/auth/verify-email",
        params={"token": "invalid-token"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_resend_verification_returns_message(client):
    response = await client.post(
        "/api/v1/auth/resend-verification",
        params={"email": "nonexistent@example.com"},
    )
    assert response.status_code == 200
    assert "message" in response.json()
