import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order_automation.schemas.automation import (
    AutomationJobCreate,
    AutomationJobRead,
    InventoryAlertCreate,
    InventoryAlertRead,
    InventoryTransactionCreate,
    InventoryTransactionRead,
    OrderEventCreate,
    OrderEventRead,
)
from app.modules.order_automation.services.automation import (
    AutomationJobService,
    InventoryAlertService,
    InventoryTransactionService,
    OrderEventService,
)
from app.shared.database.session import get_db

router = APIRouter()


@router.post("/transactions", response_model=InventoryTransactionRead, status_code=status.HTTP_201_CREATED, tags=["order-automation"])
async def create_inventory_transaction(payload: InventoryTransactionCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = InventoryTransactionService(db)
    return await service.create(**payload.model_dump())


@router.get("/transactions", response_model=list[InventoryTransactionRead], tags=["order-automation"])
async def list_inventory_transactions(
    product_id: uuid.UUID | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = InventoryTransactionService(db)
    if product_id:
        transactions, _ = await service.list_by_product(product_id, skip=skip, limit=limit)
    else:
        transactions, _ = await service.repository.get_list(skip=skip, limit=limit)
    return transactions


@router.post("/order-events", response_model=OrderEventRead, status_code=status.HTTP_201_CREATED, tags=["order-automation"])
async def create_order_event(payload: OrderEventCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = OrderEventService(db)
    return await service.create(**payload.model_dump())


@router.get("/order-events", response_model=list[OrderEventRead], tags=["order-automation"])
async def list_order_events(
    order_id: uuid.UUID | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderEventService(db)
    if order_id:
        events, _ = await service.list_by_order(order_id, skip=skip, limit=limit)
    else:
        events, _ = await service.repository.get_list(skip=skip, limit=limit)
    return events


@router.post("/jobs", response_model=AutomationJobRead, status_code=status.HTTP_201_CREATED, tags=["order-automation"])
async def create_automation_job(payload: AutomationJobCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = AutomationJobService(db)
    return await service.create(**payload.model_dump())


@router.get("/jobs", response_model=list[AutomationJobRead], tags=["order-automation"])
async def list_automation_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = AutomationJobService(db)
    jobs, _ = await service.repository.get_list(skip=skip, limit=limit)
    return jobs


@router.post("/alerts", response_model=InventoryAlertRead, status_code=status.HTTP_201_CREATED, tags=["order-automation"])
async def create_inventory_alert(payload: InventoryAlertCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = InventoryAlertService(db)
    return await service.create(**payload.model_dump())


@router.get("/alerts", response_model=list[InventoryAlertRead], tags=["order-automation"])
async def list_inventory_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = InventoryAlertService(db)
    alerts, _ = await service.list_unresolved(skip=skip, limit=limit)
    return alerts


@router.patch("/alerts/{alert_id}/resolve", response_model=InventoryAlertRead, tags=["order-automation"])
async def resolve_inventory_alert(alert_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = InventoryAlertService(db)
    alert = await service.resolve(alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return alert
