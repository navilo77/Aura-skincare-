import uuid
from typing import Any

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.schemas.order import (
    OrderCreate,
    OrderDetail,
    OrderList,
    OrderRead,
    OrderUpdate,
)
from app.modules.order.services.order import OrderService
from app.shared.database.session import get_db
from app.modules.order.models.order import Order

router = APIRouter(tags=["orders"])


@router.get("", response_model=list[OrderList])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    customer_id: uuid.UUID | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderService(db)
    orders, _ = await service.get_list(
        skip=skip, limit=limit, customer_id=customer_id, status=status, search=search
    )
    return orders


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = OrderService(db)
    order = await service.get_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = OrderService(db)
    try:
        order = await service.create(
            customer_id=payload.customer_id,
            items=payload.items,
            shipping_address=payload.shipping_address,
            billing_address=payload.billing_address,
            currency=payload.currency,
            status=payload.status,
        )
        return order
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.patch("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: uuid.UUID, payload: OrderUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = OrderService(db)
    try:
        order = await service.update(order_id=order_id, status=payload.status)
        return order
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_order(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = OrderService(db)
    try:
        await service.delete(order_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
