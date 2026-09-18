import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import RefreshToken
from app.modules.auth.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RefreshToken)

    async def get_by_jti(self, jti: str) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_jti == jti)
        )
        return result.scalar_one_or_none()

    async def get_active_by_user(self, user_id: uuid.UUID) -> list[RefreshToken]:
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False,  # noqa: E712
                RefreshToken.expires_at > datetime.utcnow(),
            )
        )
        return list(result.scalars().all())

    async def revoke_by_jti(self, jti: str) -> RefreshToken | None:
        token = await self.get_by_jti(jti)
        if token:
            token.is_revoked = True
            await self.session.flush()
        return token
