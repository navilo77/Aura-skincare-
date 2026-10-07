import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.supplier import (
    SupplierCreate,
    SupplierRead,
    SupplierUpdate,
)
from app.modules.inventory.services.supplier import SupplierService
from app.shared.database.session import get_db

router = APIRouter(tags=["suppliers"])


@router.get("", response_model=list[SupplierRead])
async def list_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = SupplierService(db)
    suppliers, _ = await service.get_list(skip=skip, limit=limit, search=search)
    return suppliers


@router.post("", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    payload: SupplierCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = SupplierService(db)
    try:
        supplier = await service.create(
            name=payload.name,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            lead_time_days=payload.lead_time_days,
            is_active=payload.is_active,
        )
        return supplier
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.get("/{supplier_id}", response_model=SupplierRead)
async def get_supplier(
    supplier_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = SupplierService(db)
    supplier = await service.get_by_id(supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
        )
    return supplier


@router.patch("/{supplier_id}", response_model=SupplierRead)
async def update_supplier(
    supplier_id: uuid.UUID, payload: SupplierUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = SupplierService(db)
    try:
        supplier = await service.update(
            supplier_id=supplier_id,
            name=payload.name,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            lead_time_days=payload.lead_time_days,
            is_active=payload.is_active,
        )
        return supplier
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_supplier(
    supplier_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = SupplierService(db)
    try:
        await service.delete(supplier_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
