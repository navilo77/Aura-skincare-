import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.schemas.brand import (
    BrandCreate,
    BrandList,
    BrandRead,
    BrandUpdate,
)
from app.modules.product.services.brand import BrandService
from app.shared.database.session import get_db
from app.modules.product.models.brand import Brand

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=list[BrandList])
async def list_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_active: bool | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BrandService(db)
    brands, _ = await service.get_list(
        skip=skip, limit=limit, is_active=is_active, search=search
    )
    return brands


@router.get("/{brand_id}", response_model=BrandRead)
async def get_brand(brand_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = BrandService(db)
    brand = await service.get_by_id(brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )
    return brand


@router.post("", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
async def create_brand(payload: BrandCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = BrandService(db)
    try:
        brand = await service.create(
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            logo_url=payload.logo_url,
        )
        return brand
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{brand_id}", response_model=BrandRead)
async def update_brand(
    brand_id: uuid.UUID,
    payload: BrandUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BrandService(db)
    try:
        brand = await service.update(
            brand_id=brand_id,
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            logo_url=payload.logo_url,
            is_active=payload.is_active,
        )
        return brand
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_brand(brand_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = BrandService(db)
    try:
        await service.delete(brand_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
