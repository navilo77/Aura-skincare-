import uuid
from typing import Any

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.schemas.product import (
    ProductCreate,
    ProductDetail,
    ProductList,
    ProductRead,
    ProductUpdate,
)
from app.modules.product.services.product import ProductService
from app.shared.database.session import get_db
from app.modules.product.models.product import Product

router = APIRouter(tags=["products"])


@router.get("", response_model=list[ProductList])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    brand_id: uuid.UUID | None = Query(None),
    category_id: uuid.UUID | None = Query(None),
    status: str | None = Query(None),
    product_type: str | None = Query(None),
    is_active: bool | None = Query(None),
    is_featured: bool | None = Query(None),
    min_price: Decimal | None = Query(None, ge=0),
    max_price: Decimal | None = Query(None, ge=0),
    search: str | None = Query(None),
    sort_by: str = Query(
        "created_at", pattern="^(name|slug|price|created_at|updated_at)$"
    ),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductService(db)
    products, _ = await service.get_list(
        skip=skip,
        limit=limit,
        brand_id=brand_id,
        category_id=category_id,
        status=status,
        product_type=product_type,
        is_active=is_active,
        is_featured=is_featured,
        min_price=min_price,
        max_price=max_price,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return products


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductService(db)
    product = await service.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductService(db)
    try:
        product = await service.create(
            brand_id=payload.brand_id,
            category_id=payload.category_id,
            name=payload.name,
            slug=payload.slug,
            sku=payload.sku,
            price=payload.price,
            currency=payload.currency,
            short_description=payload.short_description,
            description=payload.description,
            status=payload.status,
            product_type=payload.product_type,
            compare_at_price=payload.compare_at_price,
            stock_quantity=payload.stock_quantity,
            thumbnail_url=payload.thumbnail_url,
            is_featured=payload.is_featured,
            is_active=payload.is_active,
        )
        return product
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: uuid.UUID,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductService(db)
    try:
        product = await service.update(
            product_id=product_id,
            name=payload.name,
            slug=payload.slug,
            sku=payload.sku,
            short_description=payload.short_description,
            description=payload.description,
            status=payload.status,
            product_type=payload.product_type,
            price=payload.price,
            compare_at_price=payload.compare_at_price,
            currency=payload.currency,
            stock_quantity=payload.stock_quantity,
            thumbnail_url=payload.thumbnail_url,
            is_featured=payload.is_featured,
            is_active=payload.is_active,
            brand_id=payload.brand_id,
            category_id=payload.category_id,
        )
        return product
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductService(db)
    try:
        await service.delete(product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
