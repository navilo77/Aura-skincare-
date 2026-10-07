import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.auth.models.user import User
from app.modules.cart.schemas.cart import (
    CartItemCreate,
    CartItemRead,
    CartItemUpdate,
    CartRead,
    CartSummary,
)
from app.modules.cart.services.cart import CartService
from app.shared.database.session import get_db

router = APIRouter(tags=["cart"])


@router.get("", response_model=CartRead)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CartService(db)
    cart = await service.get_cart(current_user.id)
    if not cart:
        cart = await service.get_or_create_cart(current_user.id)
    items = await service.get_cart_items(current_user.id)
    return CartRead(
        id=cart.id,
        user_id=cart.user_id,
        is_active=cart.is_active,
        items=[CartItemRead.model_validate(item) for item in items],
        created_at=cart.created_at,
        updated_at=cart.updated_at,
    )


@router.post("/items", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
async def add_cart_item(
    payload: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    from app.modules.product.repositories.product import ProductRepository

    product_repository = ProductRepository(db)
    product = await product_repository.get_by_id(payload.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    service = CartService(db)
    item = await service.add_item(
        user_id=current_user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        unit_price=product.price,
        product_variant_id=payload.product_variant_id,
    )
    return CartItemRead.model_validate(item)


@router.patch("/items/{item_id}", response_model=CartItemRead)
async def update_cart_item(
    item_id: uuid.UUID,
    payload: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CartService(db)
    items = await service.get_cart_items(current_user.id)
    if not any(item.id == item_id for item in items):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )
    from app.modules.cart.repositories.cart import CartItemRepository

    item_repository = CartItemRepository(db)
    item = await item_repository.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )
    updated_item = await service.update_item(
        item_id=item_id, quantity=payload.quantity, unit_price=item.unit_price
    )
    return CartItemRead.model_validate(updated_item)


@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def remove_cart_item(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CartService(db)
    items = await service.get_cart_items(current_user.id)
    if not any(item.id == item_id for item in items):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )
    await service.remove_item(item_id)
    return None


@router.get("/summary", response_model=CartSummary)
async def get_cart_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CartService(db)
    total_items, total_amount = await service.get_cart_summary(current_user.id)
    return CartSummary(total_items=total_items, total_amount=total_amount)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CartService(db)
    await service.clear_cart(current_user.id)
    return None
