import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import NotificationTemplate
from app.modules.notification.repositories.notification import (
    NotificationTemplateRepository,
)


class TemplateService:
    def __init__(self, session: AsyncSession):
        self.repository = NotificationTemplateRepository(session)

    async def create(
        self,
        name: str,
        subject: str,
        body: str,
        channel: str,
        is_active: bool = True,
    ) -> Any:
        if await self.repository.get_by_name(name):
            raise ValueError("Template name already exists")

        template = NotificationTemplate(
            name=name,
            subject=subject,
            body=body,
            channel=channel,
            is_active=is_active,
        )
        return await self.repository.create(template)

    async def update(
        self,
        template_id: uuid.UUID,
        name: str | None = None,
        subject: str | None = None,
        body: str | None = None,
        channel: str | None = None,
        is_active: bool | None = None,
    ) -> Any:
        template = await self.repository.get_by_id(template_id)
        if not template:
            raise ValueError("Template not found")

        if name is not None:
            existing = await self.repository.get_by_name(name)
            if existing and existing.id != template_id:
                raise ValueError("Template name already exists")
            template.name = name
        if subject is not None:
            template.subject = subject
        if body is not None:
            template.body = body
        if channel is not None:
            template.channel = channel
        if is_active is not None:
            template.is_active = is_active

        return await self.repository.update(template)

    async def get_by_id(self, template_id: uuid.UUID) -> Any:
        return await self.repository.get_by_id(template_id)

    async def get_active(self, channel: str | None = None) -> Any:
        return await self.repository.get_active(channel=channel)
