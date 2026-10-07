import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.movement import MovementCreate, MovementRead
from app.modules.inventory.services.movement import MovementService
from app.shared.database.session import get_db

router = APIRouter(tags=["inventory-movements"])


@router.get("", response_model=list[MovementRead])
async def list_movements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    inventory_id: uuid.UUID | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MovementService(db)
    if inventory_id:
        movements, _ = await service.get_by_inventory(
            inventory_id, skip=skip, limit=limit
        )
    else:
        movements = []
    return movements


@router.post("", response_model=MovementRead, status_code=status.HTTP_201_CREATED)
async def create_movement(
    payload: MovementCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = MovementService(db)
    try:
        movement = await service.create(
            inventory_id=payload.inventory_id,
            movement_type=payload.movement_type,
            quantity=payload.quantity,
            reference_type=payload.reference_type,
            reference_id=payload.reference_id,
            notes=payload.notes,
        )
        return movement
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
