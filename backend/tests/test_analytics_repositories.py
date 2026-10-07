import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import AnalyticsEvent, Dashboard, Metric
from app.modules.analytics.repositories.dashboard import DashboardRepository
from app.modules.analytics.repositories.event import AnalyticsEventRepository
from app.modules.analytics.repositories.metric import MetricRepository


@pytest.mark.asyncio
async def test_event_repository(db_session: AsyncSession):
    repo = AnalyticsEventRepository(db_session)
    event = AnalyticsEvent(event_name="test_event", event_category="test")
    db_session.add(event)
    await db_session.flush()

    fetched = await repo.get_by_id(event.id)
    assert fetched is not None
    assert fetched.event_name == "test_event"

    await repo.delete(event.id)
    assert await repo.get_by_id(event.id) is None


@pytest.mark.asyncio
async def test_metric_repository(db_session: AsyncSession):
    repo = MetricRepository(db_session)
    metric = Metric(
        metric_name="test_metric",
        metric_value=10.0,
        metric_type="counter",
        recorded_at="2024-01-01",
    )
    db_session.add(metric)
    await db_session.flush()

    fetched = await repo.get_by_id(metric.id)
    assert fetched is not None
    assert fetched.metric_name == "test_metric"

    await repo.delete(metric.id)
    assert await repo.get_by_id(metric.id) is None


@pytest.mark.asyncio
async def test_dashboard_repository(db_session: AsyncSession):
    repo = DashboardRepository(db_session)
    dashboard = Dashboard(name="Test Dashboard", is_public=True)
    db_session.add(dashboard)
    await db_session.flush()

    fetched = await repo.get_by_id(dashboard.id)
    assert fetched is not None
    assert fetched.name == "Test Dashboard"

    await repo.delete(dashboard.id)
    assert await repo.get_by_id(dashboard.id) is None
