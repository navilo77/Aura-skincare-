import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import EmailVerification
from app.modules.auth.repositories.base import BaseRepository


class EmailVerificationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EmailVerification)

    async def get_by_token(self, token: str) -> EmailVerification | None:
        result = await self.session.execute(
            select(EmailVerification).where(EmailVerification.token == token)
        )
        return result.scalar_one_or_none()

    async def get_pending_by_user(self, user_id: uuid.UUID) -> EmailVerification | None:
        result = await self.session.execute(
            select(EmailVerification).where(
                EmailVerification.user_id == user_id,
                EmailVerification.verified_at.is_(None),
                EmailVerification.expires_at > datetime.utcnow(),
            )
        )
        return result.scalar_one_or_none()
