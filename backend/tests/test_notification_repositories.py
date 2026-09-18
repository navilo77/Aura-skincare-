import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import (
    Notification,
    NotificationPreference,
    NotificationTemplate,
)
from app.modules.notification.repositories.notification import (
    NotificationPreferenceRepository,
    NotificationRepository,
    NotificationTemplateRepository,
)


@pytest.mark.asyncio
async def test_template_repository(db_session: AsyncSession):
    repo = NotificationTemplateRepository(db_session)
    template = NotificationTemplate(
        name="test_template",
        subject="Test",
        body="Body",
        channel="email",
    )
    db_session.add(template)
    await db_session.flush()

    fetched = await repo.get_by_id(template.id)
    assert fetched is not None
    assert fetched.name == "test_template"

    await repo.delete(template.id)
    assert await repo.get_by_id(template.id) is None


@pytest.mark.asyncio
async def test_notification_repository(db_session: AsyncSession):
    repo = NotificationRepository(db_session)
    notification = Notification(
        user_id=uuid.uuid4(),
        channel="email",
        subject="Test",
        body="Body",
    )
    db_session.add(notification)
    await db_session.flush()

    fetched = await repo.get_by_id(notification.id)
    assert fetched is not None
    assert fetched.subject == "Test"

    await repo.delete(notification.id)
    assert await repo.get_by_id(notification.id) is None


@pytest.mark.asyncio
async def test_preference_repository(db_session: AsyncSession):
    repo = NotificationPreferenceRepository(db_session)
    preference = NotificationPreference(
        user_id=uuid.uuid4(),
        channel="email",
        is_enabled=True,
    )
    db_session.add(preference)
    await db_session.flush()

    fetched = await repo.get_by_id(preference.id)
    assert fetched is not None
    assert fetched.is_enabled is True

    await repo.delete(preference.id)
    assert await repo.get_by_id(preference.id) is None
