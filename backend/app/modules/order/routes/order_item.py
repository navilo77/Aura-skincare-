import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.rbac import Permission, require_any_permission
from app.modules.auth.models.user import User
from app.modules.order.schemas.order_item import (
    OrderItemCreateRequest,
    OrderItemList,
    OrderItemRead,
    OrderItemUpdate,
)
from app.modules.order.services.order_item import OrderItemService
from app.shared.database.session import get_db

router = APIRouter(prefix="/items", tags=["order-items"])


@router.get("", response_model=list[OrderItemList])
async def list_order_items(
    order_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderItemService(db)
    items, _ = await service.get_list(skip=skip, limit=limit, order_id=order_id)
    return items


@router.get("/{item_id}", response_model=OrderItemRead)
async def get_order_item(
    order_id: uuid.UUID,
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderItemService(db)
    item = await service.get_by_id(item_id)
    if not item or item.order_id != order_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )
    return item


@router.post("", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED)
async def create_order_item(
    order_id: uuid.UUID,
    payload: OrderItemCreateRequest,
    current_user: User = Depends(require_any_permission(Permission.ORDER_WRITE)),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderItemService(db)
    try:
        item = await service.create(
            order_id=order_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            variant_name=payload.variant_name,
        )
        return item
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.patch("/{item_id}", response_model=OrderItemRead)
async def update_order_item(
    order_id: uuid.UUID,
    item_id: uuid.UUID,
    payload: OrderItemUpdate,
    current_user: User = Depends(require_any_permission(Permission.ORDER_WRITE)),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderItemService(db)
    try:
        item = await service.get_by_id(item_id)
        if not item or item.order_id != order_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found",
            )
        updated_item = await service.update(
            item_id=item_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price,
        )
        return updated_item
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_order_item(
    order_id: uuid.UUID,
    item_id: uuid.UUID,
    current_user: User = Depends(require_any_permission(Permission.ORDER_DELETE)),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = OrderItemService(db)
    item = await service.get_by_id(item_id)
    if not item or item.order_id != order_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found",
        )
    try:
        await service.delete(item_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
