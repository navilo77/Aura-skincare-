import uuid
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.schemas.product import (
    ProductCreate,
    ProductList,
    ProductRead,
    ProductUpdate,
)
from app.modules.product.schemas.product_search_filter import ProductSearchFilter
from app.modules.product.services.product import ProductService
from app.shared.database.session import get_db

router = APIRouter(tags=["products"])


async def get_search_filters(
    brand_slug: str | None = Query(None, description="Brand slug"),
    category_slug: str | None = Query(None, description="Category slug"),
    skin_type_slug: str | None = Query(None, description="Skin type slug"),
    concern_slug: str | None = Query(None, description="Skin concern slug"),
    ingredient_slug: str | None = Query(None, description="Ingredient slug"),
    benefit_slug: str | None = Query(None, description="Benefit slug"),
    tag_slug: str | None = Query(None, description="Product tag slug"),
    routine_slug: str | None = Query(None, description="Routine type slug"),
    search: str | None = Query(None, description="Search query"),
    price_min: Decimal | None = Query(None, ge=0, description="Minimum price"),
    price_max: Decimal | None = Query(None, ge=0, description="Maximum price"),
    rating: float | None = Query(None, ge=0, le=5, description="Minimum rating"),
    availability: str | None = Query(None, description="Stock availability"),
    sort: str = Query("created_at", description="Sort field"),
    sort_order: str | None = Query("desc", description="Sort direction"),
    page: int | None = Query(1, ge=1, description="Page number"),
    limit: int | None = Query(20, ge=1, le=100, description="Items per page"),
) -> ProductSearchFilter:
    return ProductSearchFilter(
        brand_slug=brand_slug,
        category_slug=category_slug,
        skin_type_slug=skin_type_slug,
        concern_slug=concern_slug,
        ingredient_slug=ingredient_slug,
        benefit_slug=benefit_slug,
        tag_slug=tag_slug,
        routine_slug=routine_slug,
        search=search,
        price_min=price_min,
        price_max=price_max,
        rating=rating,
        availability=availability,
        sort=sort,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )


@router.get("", response_model=list[ProductList])
async def list_products(
    filters: ProductSearchFilter = Depends(get_search_filters),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ProductService(db)
    products, _ = await service.get_list(filters=filters)
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
async def create_product(
    payload: ProductCreate, db: AsyncSession = Depends(get_db)
) -> Any:
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


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_product(
    product_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = ProductService(db)
    try:
        await service.delete(product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
