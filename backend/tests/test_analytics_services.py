import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.services.dashboard import DashboardService
from app.modules.analytics.services.event import EventService
from app.modules.analytics.services.metric import MetricService


@pytest.mark.asyncio
async def test_event_service_create(db_session: AsyncSession):
    service = EventService(db_session)
    event = await service.create(
        event_name="page_view",
        event_category="engagement",
        properties='{"page": "/home"}',
    )
    assert event.id is not None
    assert event.event_name == "page_view"


@pytest.mark.asyncio
async def test_event_service_list_by_category(db_session: AsyncSession):
    service = EventService(db_session)
    await service.create(event_name="view1", event_category="engagement")
    await service.create(event_name="view2", event_category="engagement")

    events, total = await service.get_by_category("engagement")
    assert total == 2
    assert len(events) == 2


@pytest.mark.asyncio
async def test_metric_service_create(db_session: AsyncSession):
    service = MetricService(db_session)
    metric = await service.create(
        metric_name="revenue",
        metric_value=100.50,
        metric_type="counter",
    )
    assert metric.id is not None
    assert metric.metric_value == 100.50


@pytest.mark.asyncio
async def test_dashboard_service_crud(db_session: AsyncSession):
    service = DashboardService(db_session)
    dashboard = await service.create(
        name="Sales Dashboard",
        description="Sales metrics",
        is_public=True,
    )
    assert dashboard.id is not None
    assert dashboard.name == "Sales Dashboard"

    fetched = await service.get_by_id(dashboard.id)
    assert fetched is not None

    dashboards, total = await service.get_public()
    assert total == 1

    await service.repository.delete(dashboard.id)
    assert await service.get_by_id(dashboard.id) is None
