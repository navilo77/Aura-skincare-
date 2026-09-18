import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.services.notification import NotificationService
from app.modules.notification.services.preference import PreferenceService
from app.modules.notification.services.template import TemplateService


@pytest.mark.asyncio
async def test_template_service_crud(db_session: AsyncSession):
    service = TemplateService(db_session)
    template = await service.create(
        name="welcome_email",
        subject="Welcome!",
        body="Hello {{name}}",
        channel="email",
    )
    assert template.id is not None
    assert template.name == "welcome_email"

    fetched = await service.get_by_id(template.id)
    assert fetched is not None

    updated = await service.update(template_id=template.id, subject="Welcome to Aura!")
    assert updated.subject == "Welcome to Aura!"

    await service.repository.delete(template.id)
    assert await service.get_by_id(template.id) is None


@pytest.mark.asyncio
async def test_template_service_duplicate_name(db_session: AsyncSession):
    service = TemplateService(db_session)
    await service.create(
        name="dup_template",
        subject="Subject",
        body="Body",
        channel="email",
    )

    with pytest.raises(ValueError) as exc:
        await service.create(
            name="dup_template",
            subject="Subject",
            body="Body",
            channel="email",
        )
    assert "Template name already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_preference_service(db_session: AsyncSession):
    service = PreferenceService(db_session)
    pref = await service.set_preference(
        user_id=uuid.uuid4(),
        channel="email",
        is_enabled=True,
    )
    assert pref.id is not None
    assert pref.is_enabled is True

    prefs = await service.get_by_user(pref.user_id)
    assert len(prefs) == 1


@pytest.mark.asyncio
async def test_notification_service_crud(db_session: AsyncSession):
    service = NotificationService(db_session)
    notification = await service.create(
        user_id=uuid.uuid4(),
        subject="Test",
        body="Body",
        channel="email",
    )
    assert notification.id is not None
    assert notification.status == "pending"

    updated = await service.update_status(
        notification_id=notification.id,
        status="sent",
        sent_at="2024-01-01T00:00:00",
    )
    assert updated.status == "sent"
    assert updated.sent_at == "2024-01-01T00:00:00"
