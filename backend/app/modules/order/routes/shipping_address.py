import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.schemas.shipping_address import (
    ShippingAddressCreateRequest,
    ShippingAddressRead,
    ShippingAddressUpdate,
)
from app.modules.order.services.shipping_address import ShippingAddressService
from app.shared.database.session import get_db
from app.modules.order.models.shipping_address import ShippingAddress

router = APIRouter(prefix="/shipping-address", tags=["shipping-addresses"])


@router.get("", response_model=ShippingAddressRead)
async def get_shipping_address(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ShippingAddressService(db)
    address = await service.get_shipping_address(order_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping address not found",
        )
    return address


@router.post(
    "", response_model=ShippingAddressRead, status_code=status.HTTP_201_CREATED
)
async def create_shipping_address(
    order_id: uuid.UUID,
    payload: ShippingAddressCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ShippingAddressService(db)
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


@router.patch("", response_model=ShippingAddressRead)
async def update_shipping_address(
    order_id: uuid.UUID,
    payload: ShippingAddressUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ShippingAddressService(db)
    existing = await service.get_shipping_address(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping address not found",
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
async def delete_shipping_address(
    order_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = ShippingAddressService(db)
    existing = await service.get_shipping_address(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping address not found",
        )
    try:
        await service.delete(existing.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
