import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.warehouse import (
    WarehouseCreate,
    WarehouseRead,
    WarehouseUpdate,
)
from app.modules.inventory.services.warehouse import WarehouseService
from app.shared.database.session import get_db

router = APIRouter(tags=["warehouses"])


@router.get("", response_model=list[WarehouseRead])
async def list_warehouses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = WarehouseService(db)
    warehouses, _ = await service.get_list(skip=skip, limit=limit, search=search)
    return warehouses


@router.post("", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
async def create_warehouse(
    payload: WarehouseCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = WarehouseService(db)
    try:
        warehouse = await service.create(
            name=payload.name,
            code=payload.code,
            location=payload.location,
            is_active=payload.is_active,
        )
        return warehouse
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.get("/{warehouse_id}", response_model=WarehouseRead)
async def get_warehouse(
    warehouse_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = WarehouseService(db)
    warehouse = await service.get_by_id(warehouse_id)
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found"
        )
    return warehouse


@router.patch("/{warehouse_id}", response_model=WarehouseRead)
async def update_warehouse(
    warehouse_id: uuid.UUID,
    payload: WarehouseUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = WarehouseService(db)
    try:
        warehouse = await service.update(
            warehouse_id=warehouse_id,
            name=payload.name,
            code=payload.code,
            location=payload.location,
            is_active=payload.is_active,
        )
        return warehouse
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_warehouse(
    warehouse_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = WarehouseService(db)
    try:
        await service.delete(warehouse_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
