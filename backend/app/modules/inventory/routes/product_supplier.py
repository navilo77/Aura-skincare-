import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.schemas.product_supplier import (
    ProductSupplierCreate,
    ProductSupplierRead,
)
from app.modules.inventory.services.product_supplier import ProductSupplierService
from app.shared.database.session import get_db
from app.modules.inventory.models.product_supplier import ProductSupplier

router = APIRouter(tags=["product-suppliers"])


@router.get(
    "/products/{product_id}/suppliers", response_model=list[ProductSupplierRead]
)
async def list_product_suppliers(product_id: str, db: AsyncSession = Depends(get_db)) -> Any:
    service = ProductSupplierService(db)
    links = await service.get_by_product(uuid.UUID(product_id))
    return links


@router.post(
    "/products/{product_id}/suppliers",
    response_model=ProductSupplierRead,
    status_code=status.HTTP_201_CREATED,
)
async def link_product_supplier(
    product_id: str, payload: ProductSupplierCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = ProductSupplierService(db)
    try:
        link = await service.create(
            product_id=uuid.UUID(product_id),
            supplier_id=payload.supplier_id,
            cost_price=payload.cost_price,
            is_preferred=payload.is_preferred,
        )
        return link
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/products/{product_id}/suppliers/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def unlink_product_supplier(
    product_id: str, supplier_id: str, db: AsyncSession = Depends(get_db)
) -> Any:
    service = ProductSupplierService(db)
    try:
        await service.delete(uuid.UUID(product_id), uuid.UUID(supplier_id))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
