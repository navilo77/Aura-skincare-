import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import PasswordResetToken
from app.modules.auth.repositories.base import BaseRepository


class PasswordResetTokenRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PasswordResetToken)

    async def get_by_token(self, token: str) -> PasswordResetToken | None:
        result = await self.session.execute(
            select(PasswordResetToken).where(PasswordResetToken.token == token)
        )
        return result.scalar_one_or_none()

    async def get_valid_by_user(self, user_id: uuid.UUID) -> PasswordResetToken | None:
        result = await self.session.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used_at.is_(None),
                PasswordResetToken.expires_at > datetime.utcnow(),
            )
        )
        return result.scalar_one_or_none()

    async def invalidate_previous(self, user_id: uuid.UUID) -> None:
        result = await self.session.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used_at.is_(None),
            )
        )
        for token in result.scalars().all():
            token.used_at = datetime.utcnow()
        await self.session.flush()
