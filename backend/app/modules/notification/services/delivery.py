import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.integrations.email import sendgrid_client
from app.integrations.n8n import n8n_client
from app.modules.notification.models import (
    Notification,
)
from app.modules.notification.repositories.notification import (
    NotificationPreferenceRepository,
    NotificationRepository,
    NotificationTemplateRepository,
)


class NotificationDeliveryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.notification_repo = NotificationRepository(session)
        self.template_repo = NotificationTemplateRepository(session)
        self.preference_repo = NotificationPreferenceRepository(session)

    async def send_notification(self, notification_id: uuid.UUID) -> bool:
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            return False

        # Check user preferences
        preference = await self.preference_repo.get_by_user_and_channel(
            notification.user_id, notification.channel
        )
        if preference and not preference.is_enabled:
            notification.status = "cancelled"
            await self.session.flush()
            return False

        success = False
        error_message = None

        try:
            if notification.channel == "email":
                success = await self._send_email(notification)
            elif notification.channel == "sms":
                success = await self._send_sms(notification)
            elif notification.channel == "push":
                success = await self._send_push(notification)
            elif notification.channel == "whatsapp":
                success = await self._send_whatsapp(notification)
            else:
                success = await self._send_generic(notification)

        except Exception as e:
            error_message = str(e)
            success = False

        if success:
            notification.status = "sent"
            notification.sent_at = datetime.utcnow()
            notification.error_message = None
        else:
            notification.retry_count += 1
            notification.error_message = error_message

            if notification.retry_count >= notification.max_retries:
                notification.status = "failed"
            else:
                notification.status = "pending"
                # Exponential backoff: 5min, 15min, 45min, ...
                delay_minutes = 5 * (3 ** (notification.retry_count - 1))
                notification.next_retry_at = datetime.utcnow() + timedelta(
                    minutes=delay_minutes
                )

        await self.session.flush()
        return success

    async def _send_email(self, notification: Notification) -> bool:
        if sendgrid_client is None:
            raise RuntimeError("Email provider is disabled")

        # Get user email
        from app.modules.auth.models.user import User

        stmt = select(User).where(User.id == notification.user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.email:
            return False

        result = sendgrid_client.send_email(
            to_email=user.email,
            subject=notification.subject,
            html_content=notification.body,
        )
        return result.get("success", False)

    async def _send_sms(self, notification: Notification) -> bool:
        # TODO: Implement SMS provider (Twilio, etc.)
        # For now, trigger n8n webhook
        return await self._trigger_n8n_webhook(notification, "sms")

    async def _send_push(self, notification: Notification) -> bool:
        # TODO: Implement push notification (Firebase, etc.)
        return await self._trigger_n8n_webhook(notification, "push")

    async def _send_whatsapp(self, notification: Notification) -> bool:
        # TODO: Implement WhatsApp provider
        return await self._trigger_n8n_webhook(notification, "whatsapp")

    async def _send_generic(self, notification: Notification) -> bool:
        return await self._trigger_n8n_webhook(notification, notification.channel)

    async def _trigger_n8n_webhook(
        self, notification: Notification, channel: str
    ) -> bool:
        webhook_url = f"{settings.n8n_webhook_url}/notification/{channel}"
        payload = {
            "notification_id": str(notification.id),
            "user_id": str(notification.user_id),
            "channel": channel,
            "subject": notification.subject,
            "body": notification.body,
            "template_id": str(notification.template_id)
            if notification.template_id
            else None,
        }
        result = await n8n_client.trigger_webhook(webhook_url, payload)
        return result.get("success", False)

    async def retry_pending_notifications(self) -> int:
        """Process notifications that are ready for retry"""
        stmt = select(Notification).where(
            Notification.status == "pending",
            Notification.next_retry_at.isnot(None),
            Notification.next_retry_at <= datetime.utcnow(),
            Notification.retry_count < Notification.max_retries,
        )
        result = await self.session.execute(stmt)
        notifications = result.scalars().all()

        sent_count = 0
        for notification in notifications:
            if await self.send_notification(notification.id):
                sent_count += 1

        return sent_count

    async def process_pending_notifications(self, limit: int = 100) -> int:
        """Process all pending notifications"""
        stmt = (
            select(Notification)
            .where(
                Notification.status == "pending",
                (Notification.next_retry_at.is_(None))
                | (Notification.next_retry_at <= datetime.utcnow()),
            )
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        notifications = result.scalars().all()

        sent_count = 0
        for notification in notifications:
            if await self.send_notification(notification.id):
                sent_count += 1

        return sent_count


# NotificationService has been moved to services/notification.py
# This file contains only NotificationDeliveryService (channel-level dispatch)
