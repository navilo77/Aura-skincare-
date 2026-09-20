import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.auth.models.user import User
from app.modules.order.repositories.order import OrderRepository
from app.shared.database.session import get_db

router = APIRouter(tags=["profile-orders"])


@router.get("", response_model=list[dict[str, Any]])
async def list_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    repository = OrderRepository(db)
    orders, _ = await repository.get_list(
        skip=skip,
        limit=limit,
        customer_id=current_user.id,
    )
    return [
        {
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": order.total_amount,
            "currency": order.currency,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }
        for order in orders
    ]


@router.get("/{order_id}", response_model=dict[str, Any])
async def get_my_order(
    order_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    repository = OrderRepository(db)
    order = await repository.get_by_id(order_id)
    if not order or order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_id": order.customer_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "currency": order.currency,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }
