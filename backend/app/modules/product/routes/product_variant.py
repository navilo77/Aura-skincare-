import uuid
from typing import Any

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.schemas.product_variant import (
    ProductVariantCreateRequest,
    ProductVariantRead,
    ProductVariantUpdate,
)
from app.modules.product.services.product_variant import ProductVariantService
from app.shared.database.session import get_db
from app.modules.product.models.product_variant import ProductVariant

router = APIRouter(prefix="/variants", tags=["product-variants"])


@router.get("", response_model=list[ProductVariantRead])
async def list_variants(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    product_id: uuid.UUID | None = Query(None),
    is_active: bool | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductVariantService(db)
    variants, _ = await service.get_list(
        skip=skip,
        limit=limit,
        product_id=product_id,
        is_active=is_active,
        search=search,
    )
    return variants


@router.get("/{variant_id}", response_model=ProductVariantRead)
async def get_variant(variant_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductVariantService(db)
    variant = await service.get_by_id(variant_id)
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    return variant


@router.post(
    "/{product_id}",
    response_model=ProductVariantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_variant(
    product_id: uuid.UUID,
    payload: ProductVariantCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductVariantService(db)
    try:
        variant = await service.create(
            product_id=product_id,
            name=payload.name,
            sku=payload.sku,
            price=payload.price,
            stock_quantity=payload.stock_quantity,
            attributes=payload.attributes,
            is_active=payload.is_active,
        )
        return variant
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{variant_id}", response_model=ProductVariantRead)
async def update_variant(
    variant_id: uuid.UUID,
    payload: ProductVariantUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductVariantService(db)
    try:
        variant = await service.update(
            variant_id=variant_id,
            name=payload.name,
            sku=payload.sku,
            price=payload.price,
            stock_quantity=payload.stock_quantity,
            attributes=payload.attributes,
            is_active=payload.is_active,
        )
        return variant
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_variant(variant_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductVariantService(db)
    try:
        await service.delete(variant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
