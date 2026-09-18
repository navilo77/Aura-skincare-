from typing import Any


from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.schemas.analytics import (
    DashboardCreate,
    DashboardRead,
    MetricCreate,
    MetricRead,
)
from app.modules.analytics.services.dashboard import DashboardService
from app.modules.analytics.services.metric import MetricService
from app.shared.database.session import get_db
from app.modules.analytics.models.analytics import Dashboard, Metric

router = APIRouter(tags=["analytics"])


@router.get("/dashboards", response_model=list[DashboardRead])
async def list_dashboards(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = DashboardService(db)
    dashboards, _ = await service.get_public(skip=skip, limit=limit)
    return dashboards


@router.post(
    "/dashboards", response_model=DashboardRead, status_code=status.HTTP_201_CREATED
)
async def create_dashboard(
    payload: DashboardCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = DashboardService(db)
    dashboard = await service.create(
        name=payload.name,
        description=payload.description,
        is_public=payload.is_public,
        layout=payload.layout,
    )
    return dashboard


@router.get("/metrics", response_model=list[MetricRead])
async def list_metrics(
    name: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MetricService(db)
    if name:
        metrics, _ = await service.get_by_name(name, skip=skip, limit=limit)
    else:
        metrics = []
    return metrics


@router.post("/metrics", response_model=MetricRead, status_code=status.HTTP_201_CREATED)
async def create_metric(payload: MetricCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = MetricService(db)
    metric = await service.create(
        metric_name=payload.metric_name,
        metric_value=payload.metric_value,
        metric_type=payload.metric_type,
        dimensions=payload.dimensions,
        recorded_at=payload.recorded_at,
    )
    return metric
