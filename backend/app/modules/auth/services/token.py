import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.modules.auth.models import RefreshToken
from app.modules.auth.repositories.refresh_token import RefreshTokenRepository
from app.shared.security.jwt import decode_token


class TokenService:
    def __init__(self, session: AsyncSession) -> None:
        self.refresh_repository = RefreshTokenRepository(session)

    def create_access_token(self, user_id: uuid.UUID, role: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
            "iat": now,
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    def create_refresh_token(self, user_id: uuid.UUID) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "exp": now + timedelta(days=30),
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    def decode_token(self, token: str) -> dict[str, Any] | None:
        try:
            return decode_token(token)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            ) from exc

    async def create_refresh_token_record(
        self, user_id: uuid.UUID, jti: str, expires_at: datetime
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_jti=jti,
            expires_at=expires_at,
        )
        return await self.refresh_repository.create(token)  # type: ignore[no-any-return]

    async def revoke_refresh_token(self, jti: str) -> None:
        await self.refresh_repository.revoke_by_jti(jti)

    async def get_active_refresh_tokens(self, user_id: uuid.UUID) -> list[RefreshToken]:
        return await self.refresh_repository.get_active_by_user(user_id)
