import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.rbac import Permission, require_any_permission
from app.modules.auth.models.user import User
from app.modules.order.schemas.order import (
    OrderCreate,
    OrderList,
    OrderRead,
    OrderUpdate,
)
from app.modules.order.services.order import OrderService
from app.shared.database.session import get_db

router = APIRouter(tags=["orders"])


@router.get("", response_model=list[OrderList])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    customer_id: uuid.UUID | None = Query(None),
    order_status: str | None = Query(None, alias="status"),
    search: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderService(db)
    # Customers can only see their own orders
    filter_customer_id = customer_id
    if current_user.role == "customer":
        filter_customer_id = current_user.id
    orders, _ = await service.get_list(
        skip=skip,
        limit=limit,
        customer_id=filter_customer_id,
        status=order_status,
        search=search,
    )
    return orders


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderService(db)
    order = await service.get_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    # Customers can only view their own orders
    if current_user.role == "customer" and order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return order


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderService(db)
    try:
        order = await service.create(
            customer_id=payload.customer_id or current_user.id,
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
    order_id: uuid.UUID,
    payload: OrderUpdate,
    current_user: User = Depends(require_any_permission(Permission.ORDER_WRITE)),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderService(db)
    try:
        order = await service.update(order_id=order_id, status=payload.status)
        return order
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_order(
    order_id: uuid.UUID,
    current_user: User = Depends(require_any_permission(Permission.ORDER_DELETE)),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderService(db)
    try:
        await service.delete(order_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
