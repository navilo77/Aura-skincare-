import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.schemas.product_image import (
    ProductImageCreateRequest,
    ProductImageRead,
    ProductImageUpdate,
)
from app.modules.product.services.product_image import ProductImageService
from app.shared.database.session import get_db

router = APIRouter(prefix="/images", tags=["product-images"])


@router.get("", response_model=list[ProductImageRead])
async def list_images(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    product_id: uuid.UUID | None = Query(None),
    is_primary: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductImageService(db)
    images, _ = await service.get_list(
        skip=skip,
        limit=limit,
        product_id=product_id,
        is_primary=is_primary,
    )
    return images


@router.get("/{image_id}", response_model=ProductImageRead)
async def get_image(image_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductImageService(db)
    image = await service.get_by_id(image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product image not found",
        )
    return image


@router.post(
    "/{product_id}",
    response_model=ProductImageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_image(
    product_id: uuid.UUID,
    payload: ProductImageCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductImageService(db)
    try:
        image = await service.create(
            product_id=product_id,
            image_url=payload.image_url,
            alt_text=payload.alt_text,
            sort_order=payload.sort_order,
            is_primary=payload.is_primary,
        )
        return image
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{image_id}", response_model=ProductImageRead)
async def update_image(
    image_id: uuid.UUID,
    payload: ProductImageUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductImageService(db)
    try:
        image = await service.update(
            image_id=image_id,
            image_url=payload.image_url,
            alt_text=payload.alt_text,
            sort_order=payload.sort_order,
            is_primary=payload.is_primary,
        )
        return image
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{image_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_image(image_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductImageService(db)
    try:
        await service.delete(image_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
