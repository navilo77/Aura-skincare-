import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.reservation import (
    ReservationCreate,
    ReservationRead,
    ReservationRelease,
)
from app.modules.inventory.services.reservation import ReservationService
from app.shared.database.session import get_db
from app.modules.inventory.models.reservation import InventoryReservation

router = APIRouter(tags=["inventory-reservations"])


@router.get("", response_model=list[ReservationRead])
async def list_reservations(
    inventory_id: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ReservationService(db)
    if inventory_id:
        reservations = await service.get_by_inventory(uuid.UUID(inventory_id))
    else:
        reservations = []
    return reservations


@router.post("", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    payload: ReservationCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = ReservationService(db)
    try:
        reservation = await service.create(
            inventory_id=payload.inventory_id,
            order_item_id=payload.order_item_id,
            quantity=payload.quantity,
        )
        return reservation
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.post("/{reservation_id}/release", response_model=ReservationRead)
async def release_reservation(
    reservation_id: str, payload: ReservationRelease, db: AsyncSession = Depends(get_db)
) -> Any:
    service = ReservationService(db)
    try:
        reservation = await service.release(uuid.UUID(reservation_id))
        return reservation
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
