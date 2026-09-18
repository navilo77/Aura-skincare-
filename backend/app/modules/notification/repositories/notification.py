import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import (
    Notification,
    NotificationPreference,
    NotificationTemplate,
)
from app.modules.notification.repositories.base import BaseRepository


class NotificationTemplateRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NotificationTemplate)

    async def get_by_name(self, name: str) -> NotificationTemplate | None:
        result = await self.session.execute(
            select(NotificationTemplate).where(NotificationTemplate.name == name)
        )
        return result.scalar_one_or_none()

    async def get_active(self, channel: str | None = None) -> list[Any]:
        query = select(NotificationTemplate).where(
            NotificationTemplate.is_active == True  # noqa: E712
        )
        if channel:
            query = query.where(NotificationTemplate.channel == channel)
        result = await self.session.execute(query)
        return list(result.scalars().all())


class NotificationPreferenceRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NotificationPreference)

    async def get_by_user_and_channel(
        self, user_id: uuid.UUID, channel: str
    ) -> NotificationPreference | None:
        result = await self.session.execute(
            select(NotificationPreference).where(
                NotificationPreference.user_id == user_id,
                NotificationPreference.channel == channel,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: uuid.UUID) -> list[NotificationPreference]:
        result = await self.session.execute(
            select(NotificationPreference).where(
                NotificationPreference.user_id == user_id
            )
        )
        return list(result.scalars().all())


class NotificationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Notification)

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> tuple[list[Any], int]:
        query = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total

    async def get_by_status(self, status: str, skip: int = 0, limit: int = 20) -> tuple[list[Any], int]:
        query = (
            select(Notification)
            .where(Notification.status == status)
            .order_by(Notification.created_at.desc())
        )
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total
