import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.auth.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_email_excluding_id(
        self, email: str, user_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(User).where(User.email == email.lower(), User.id != user_id)
        )
        return result.scalar_one_or_none() is not None
