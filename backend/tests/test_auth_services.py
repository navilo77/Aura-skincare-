import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.auth.repositories.user import UserRepository
from app.modules.auth.services.auth import AuthService


@pytest.mark.asyncio
async def test_user_repository_crud(db_session: AsyncSession):
    repo = UserRepository(db_session)
    user = User(
        email="test@example.com",
        password_hash="hashed",
        full_name="Test User",
        role="customer",
    )
    db_session.add(user)
    await db_session.flush()

    fetched = await repo.get_by_id(user.id)
    assert fetched is not None
    assert fetched.email == "test@example.com"

    by_email = await repo.get_by_email("test@example.com")
    assert by_email is not None
    assert by_email.id == user.id

    assert await repo.exists_by_email("test@example.com") is True

    await repo.delete(user.id)
    assert await repo.get_by_id(user.id) is None


@pytest.mark.asyncio
async def test_user_repository_duplicate_email(db_session: AsyncSession):
    repo = UserRepository(db_session)
    user = User(email="dup@example.com", password_hash="hashed", full_name="User")
    db_session.add(user)
    await db_session.flush()

    assert await repo.exists_by_email("dup@example.com") is True
    assert await repo.exists_by_email_excluding_id(
        "dup@example.com", uuid.uuid4()
    ) is True
    assert await repo.exists_by_email_excluding_id("dup@example.com", user.id) is False


@pytest.mark.asyncio
async def test_auth_service_register(db_session: AsyncSession):
    service = AuthService(db_session)
    user = await service.register(
        email="auth@example.com",
        password="secure123",
        full_name="Auth User",
    )
    assert user.id is not None
    assert user.email == "auth@example.com"
    assert user.role == "customer"


@pytest.mark.asyncio
async def test_auth_service_register_duplicate(db_session: AsyncSession):
    service = AuthService(db_session)
    await service.register(
        email="dup@example.com",
        password="secure123",
        full_name="User",
    )

    with pytest.raises(ValueError) as exc:
        await service.register(
            email="dup@example.com",
            password="secure123",
            full_name="User",
        )
    assert "Email already registered" in str(exc.value)


@pytest.mark.asyncio
async def test_auth_service_login(db_session: AsyncSession):
    service = AuthService(db_session)
    await service.register(
        email="login@example.com",
        password="secure123",
        full_name="Login User",
    )

    user, access_token, refresh_token = await service.login(
        "login@example.com", "secure123"
    )
    assert user is not None
    assert access_token is not None
    assert refresh_token is not None


@pytest.mark.asyncio
async def test_auth_service_login_invalid(db_session: AsyncSession):
    service = AuthService(db_session)

    with pytest.raises(ValueError) as exc:
        await service.login("nonexistent@example.com", "wrong")
    assert "Invalid email or password" in str(exc.value)
