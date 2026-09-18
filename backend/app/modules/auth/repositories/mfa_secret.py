import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import MfaSecret
from app.modules.auth.repositories.base import BaseRepository


class MfaSecretRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MfaSecret)

    async def get_by_user(self, user_id: uuid.UUID) -> MfaSecret | None:
        result = await self.session.execute(
            select(MfaSecret).where(MfaSecret.user_id == user_id)
        )
        return result.scalar_one_or_none()
