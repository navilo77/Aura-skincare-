import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.inventory import (
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
)
from app.modules.inventory.services.inventory import InventoryService
from app.shared.database.session import get_db

router = APIRouter(tags=["inventory"])


@router.get("/products/{product_id}", response_model=InventoryRead)
async def get_inventory_by_product(
    product_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = InventoryService(db)
    inventory = await service.get_by_product(product_id)
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found"
        )
    return inventory


@router.patch("/products/{product_id}", response_model=InventoryRead)
async def update_inventory(
    product_id: uuid.UUID, payload: InventoryUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = InventoryService(db)
    try:
        inventory = await service.update(
            product_id=product_id,
            low_stock_threshold=payload.low_stock_threshold,
            is_tracking_enabled=payload.is_tracking_enabled,
        )
        return inventory
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("", response_model=list[InventoryRead])
async def list_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    warehouse_id: uuid.UUID | None = Query(None),
    low_stock_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = InventoryService(db)
    inventories, _ = await service.get_list(
        skip=skip,
        limit=limit,
        warehouse_id=warehouse_id,
        low_stock_only=low_stock_only,
    )
    return inventories


@router.post("", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    payload: InventoryCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = InventoryService(db)
    try:
        inventory = await service.create(
            product_id=payload.product_id,
            warehouse_id=payload.warehouse_id,
            quantity_on_hand=payload.quantity_on_hand,
            quantity_reserved=payload.quantity_reserved,
            low_stock_threshold=payload.low_stock_threshold,
            is_tracking_enabled=payload.is_tracking_enabled,
        )
        return inventory
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
