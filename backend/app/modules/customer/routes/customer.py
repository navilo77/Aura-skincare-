import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customer.schemas.customer import (
    CustomerCreate,
    CustomerDetail,
    CustomerList,
    CustomerRead,
    CustomerUpdate,
)
from app.modules.customer.models.customer import Customer
from app.modules.customer.services.customer import CustomerService
from app.shared.database.session import get_db

router = APIRouter(tags=["customers"])


@router.get("", response_model=list[CustomerList])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CustomerService(db)
    customers, _ = await service.get_list(
        skip=skip, limit=limit, status=status, search=search
    )
    return customers


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = CustomerService(db)
    customer = await service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


@router.post(
    "", response_model=CustomerRead, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    payload: CustomerCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = CustomerService(db)
    try:
        customer = await service.create(
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
            status=payload.status,
            skin_type=payload.skin_type,
            skin_concerns=payload.skin_concerns,
        )
        return customer
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.patch("/{customer_id}", response_model=CustomerRead)
async def update_customer(
    customer_id: uuid.UUID,
    payload: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CustomerService(db)
    try:
        customer = await service.update(
            customer_id=customer_id,
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
            status=payload.status,
            skin_type=payload.skin_type,
            skin_concerns=payload.skin_concerns,
        )
        return customer
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_customer(
    customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = CustomerService(db)
    try:
        await service.delete(customer_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
