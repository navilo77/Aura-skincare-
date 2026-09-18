import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import Notification
from app.modules.notification.repositories.notification import NotificationRepository
from typing import Any



class NotificationService:
    def __init__(self, session: AsyncSession):
        self.repository = NotificationRepository(session)

    async def create(
        self,
        user_id: uuid.UUID,
        subject: str,
        body: str,
        channel: str,
        template_id: uuid.UUID | None = None,
    ) -> Any:
        notification = Notification(
            user_id=user_id,
            template_id=template_id,
            channel=channel,
            subject=subject,
            body=body,
            status="pending",
        )
        return await self.repository.create(notification)

    async def update_status(
        self,
        notification_id: uuid.UUID,
        status: str,
        error_message: str | None = None,
        sent_at: str | None = None,
    ) -> Any:
        notification = await self.repository.get_by_id(notification_id)
        if not notification:
            raise ValueError("Notification not found")

        notification.status = status
        if error_message is not None:
            notification.error_message = error_message
        if sent_at is not None:
            notification.sent_at = sent_at

        return await self.repository.update(notification)

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_by_user(user_id, skip=skip, limit=limit)

    async def get_by_status(self, status: str, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_by_status(status, skip=skip, limit=limit)
