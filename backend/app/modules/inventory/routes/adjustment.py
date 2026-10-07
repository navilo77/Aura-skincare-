import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.adjustment import (
    AdjustmentApprove,
    AdjustmentCreate,
    AdjustmentRead,
)
from app.modules.inventory.services.adjustment import AdjustmentService
from app.shared.database.session import get_db

router = APIRouter(tags=["inventory-adjustments"])


@router.get("", response_model=list[AdjustmentRead])
async def list_adjustments(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = AdjustmentService(db)
    adjustments, _ = await service.get_pending(skip=skip, limit=limit)
    return adjustments


@router.post("", response_model=AdjustmentRead, status_code=status.HTTP_201_CREATED)
async def create_adjustment(
    payload: AdjustmentCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = AdjustmentService(db)
    try:
        adjustment = await service.create(
            inventory_id=payload.inventory_id,
            adjustment_type=payload.adjustment_type,
            quantity_change=payload.quantity_change,
            reason=payload.reason,
        )
        return adjustment
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.post("/{adjustment_id}/approve", response_model=AdjustmentRead)
async def approve_adjustment(
    adjustment_id: str, payload: AdjustmentApprove, db: AsyncSession = Depends(get_db)
) -> Any:
    service = AdjustmentService(db)
    try:
        adjustment = await service.approve(
            adjustment_id=uuid.UUID(adjustment_id),
            approved=payload.approved,
            approved_by=None,
        )
        return adjustment
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
