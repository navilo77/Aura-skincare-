"""
NotificationService — canonical service for notification CRUD + delivery.
delivery.py houses NotificationDeliveryService (low-level channel dispatch).
This module is the single import point for route handlers.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import Notification
from app.modules.notification.repositories.notification import (
    NotificationPreferenceRepository,
    NotificationRepository,
    NotificationTemplateRepository,
)
from app.modules.notification.services.delivery import NotificationDeliveryService


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.notification_repo = NotificationRepository(session)
        self.template_repo = NotificationTemplateRepository(session)
        self.preference_repo = NotificationPreferenceRepository(session)
        self.delivery_service = NotificationDeliveryService(session)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def create(
        self,
        user_id: uuid.UUID,
        subject: str,
        body: str,
        channel: str,
        template_id: uuid.UUID | None = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            template_id=template_id,
            channel=channel,
            subject=subject,
            body=body,
            status="pending",
        )
        created = await self.notification_repo.create(notification)
        # Try to send immediately; failure is non-fatal
        await self.delivery_service.send_notification(created.id)
        return created

    async def create_from_template(
        self,
        user_id: uuid.UUID,
        template_name: str,
        variables: dict[str, Any] | None = None,
        channel: str | None = None,
    ) -> Notification | None:
        if variables is None:
            variables = {}

        template = await self.template_repo.get_by_name(template_name)
        if not template or not template.is_active:
            return None

        send_channel = channel or template.channel

        # Simple {{variable}} substitution
        subject = template.subject
        body = template.body
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))

        return await self.create(
            user_id=user_id,
            subject=subject,
            body=body,
            channel=send_channel,
            template_id=template.id,
        )

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def get_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[Any], int]:
        return await self.notification_repo.get_by_user(user_id, skip=skip, limit=limit)

    async def get_by_status(
        self, status: str, skip: int = 0, limit: int = 20
    ) -> tuple[list[Any], int]:
        return await self.notification_repo.get_by_status(
            status, skip=skip, limit=limit
        )

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    async def update_status(
        self,
        notification_id: uuid.UUID,
        status: str,
        error_message: str | None = None,
        sent_at: datetime | None = None,
    ) -> Notification:
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise ValueError("Notification not found")

        notification.status = status
        if error_message is not None:
            notification.error_message = error_message
        if sent_at is not None:
            notification.sent_at = sent_at

        return await self.notification_repo.update(notification)

    # ------------------------------------------------------------------
    # Delivery helpers
    # ------------------------------------------------------------------

    async def send_now(self, notification_id: uuid.UUID) -> bool:
        return await self.delivery_service.send_notification(notification_id)

    async def retry_failed(self, notification_id: uuid.UUID) -> bool:
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            return False

        notification.retry_count = 0
        notification.status = "pending"
        notification.next_retry_at = None
        notification.error_message = None
        await self.session.flush()

        return await self.delivery_service.send_notification(notification_id)
