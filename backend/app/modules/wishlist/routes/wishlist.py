import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.auth.models.user import User
from app.modules.product.repositories.product import ProductRepository
from app.modules.wishlist.schemas.wishlist import WishlistItemRead, WishlistRead
from app.modules.wishlist.services.wishlist import WishlistService
from app.shared.database.session import get_db

router = APIRouter(tags=["wishlist"])


@router.get("", response_model=WishlistRead)
async def get_wishlist(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = WishlistService(db)
    wishlist = await service.get_wishlist(current_user.id)
    if not wishlist:
        wishlist = await service.get_or_create_wishlist(current_user.id)
    items = await service.get_wishlist_items(current_user.id)
    return WishlistRead(
        id=wishlist.id,
        user_id=wishlist.user_id,
        is_active=wishlist.is_active,
        items=[WishlistItemRead.model_validate(item) for item in items],
        created_at=wishlist.created_at,
        updated_at=wishlist.updated_at,
    )


@router.post(
    "/items/{product_id}",
    response_model=WishlistItemRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_wishlist_item(
    product_id: uuid.UUID,
    product_variant_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    product_repository = ProductRepository(db)
    product = await product_repository.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    service = WishlistService(db)
    item = await service.add_item(
        user_id=current_user.id,
        product_id=product_id,
        product_variant_id=product_variant_id,
    )
    return WishlistItemRead.model_validate(item)


@router.delete(
    "/items/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def remove_wishlist_item(
    product_id: uuid.UUID,
    product_variant_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = WishlistService(db)
    await service.remove_item(
        user_id=current_user.id,
        product_id=product_id,
        product_variant_id=product_variant_id,
    )
    return None
