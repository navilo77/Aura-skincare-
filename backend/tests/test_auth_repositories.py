import uuid
from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import RefreshToken
from app.modules.auth.repositories.refresh_token import RefreshTokenRepository
from app.modules.auth.services.token import TokenService


@pytest.mark.asyncio
async def test_refresh_token_repository(db_session: AsyncSession):
    repo = RefreshTokenRepository(db_session)
    token = RefreshToken(
        user_id=uuid.uuid4(),
        token_jti="jti-123",
        expires_at=datetime(2099, 1, 1),
    )
    db_session.add(token)
    await db_session.flush()

    fetched = await repo.get_by_jti("jti-123")
    assert fetched is not None
    assert fetched.is_revoked is False

    await repo.revoke_by_jti("jti-123")
    revoked = await repo.get_by_jti("jti-123")
    assert revoked.is_revoked is True

    await repo.delete(token.id)
    assert await repo.get_by_jti("jti-123") is None


@pytest.mark.asyncio
async def test_token_service_create_and_revoke(db_session: AsyncSession):
    token_service = TokenService(db_session)
    access_token = token_service.create_access_token(uuid.uuid4(), "customer")
    assert access_token is not None

    refresh_token = token_service.create_refresh_token(uuid.uuid4())
    assert refresh_token is not None
