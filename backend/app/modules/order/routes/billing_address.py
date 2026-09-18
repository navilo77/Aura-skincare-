import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.schemas.billing_address import (
    BillingAddressCreateRequest,
    BillingAddressRead,
    BillingAddressUpdate,
)
from app.modules.order.services.billing_address import BillingAddressService
from app.shared.database.session import get_db
from app.modules.order.models.billing_address import BillingAddress

router = APIRouter(prefix="/billing-address", tags=["billing-addresses"])


@router.get("", response_model=BillingAddressRead)
async def get_billing_address(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = BillingAddressService(db)
    address = await service.get_billing_address(order_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Billing address not found"
        )
    return address


@router.post(
    "", response_model=BillingAddressRead, status_code=status.HTTP_201_CREATED
)
async def create_billing_address(
    order_id: uuid.UUID,
    payload: BillingAddressCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BillingAddressService(db)
    try:
        address = await service.create(
            order_id=order_id,
            full_name=payload.full_name,
            phone=payload.phone,
            address_line1=payload.address_line1,
            address_line2=payload.address_line2,
            city=payload.city,
            state=payload.state,
            postal_code=payload.postal_code,
            country=payload.country,
        )
        return address
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.patch("", response_model=BillingAddressRead)
async def update_billing_address(
    order_id: uuid.UUID,
    payload: BillingAddressUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BillingAddressService(db)
    existing = await service.get_billing_address(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Billing address not found"
        )
    try:
        address = await service.update(
            address_id=existing.id,
            full_name=payload.full_name,
            phone=payload.phone,
            address_line1=payload.address_line1,
            address_line2=payload.address_line2,
            city=payload.city,
            state=payload.state,
            postal_code=payload.postal_code,
            country=payload.country,
        )
        return address
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_billing_address(
    order_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = BillingAddressService(db)
    existing = await service.get_billing_address(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Billing address not found"
        )
    try:
        await service.delete(existing.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
