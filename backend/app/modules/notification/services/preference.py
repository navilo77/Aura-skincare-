import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import NotificationPreference
from app.modules.notification.repositories.notification import (
    NotificationPreferenceRepository,
)


class PreferenceService:
    def __init__(self, session: AsyncSession):
        self.repository = NotificationPreferenceRepository(session)

    async def set_preference(
        self, user_id: uuid.UUID, channel: str, is_enabled: bool
    ) -> Any:
        existing = await self.repository.get_by_user_and_channel(user_id, channel)
        if existing:
            existing.is_enabled = is_enabled
            return await self.repository.update(existing)

        preference = NotificationPreference(
            user_id=user_id,
            channel=channel,
            is_enabled=is_enabled,
        )
        return await self.repository.create(preference)

    async def get_by_user(self, user_id: uuid.UUID) -> Any:
        return await self.repository.get_by_user(user_id)

    async def get_by_channel(self, user_id: uuid.UUID, channel: str) -> Any:
        return await self.repository.get_by_user_and_channel(user_id, channel)
