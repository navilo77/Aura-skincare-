import uuid
from decimal import Decimal
from typing import Any

# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customer.repositories.customer import CustomerRepository
from app.modules.order.schemas.order import OrderCreate
from app.modules.order.services.order import OrderService
from app.shared.database.session import get_db

router = APIRouter()


class CheckoutItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    quantity: int = Field(..., ge=1)


class CheckoutShippingAddress(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address_line1: str = Field(..., min_length=1)
    address_line2: str | None = None
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2, max_length=2)
    phone: str | None = None


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    full_name: str = Field(..., min_length=1)
    phone: str | None = None
    items: list[CheckoutItem] = Field(..., min_length=1)
    shipping_address: CheckoutShippingAddress
    currency: str = Field("USD", min_length=3, max_length=3)


class CheckoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_number: str
    order_id: uuid.UUID
    status: str
    total_amount: Decimal
    currency: str


async def get_or_create_customer(
    db: AsyncSession,
    email: str,
    full_name: str,
    phone: str | None = None,
) -> uuid.UUID:
    customer_repo = CustomerRepository(db)
    customer = await customer_repo.get_by_email(email)
    if customer:
        return uuid.UUID(str(customer.id))

    from app.modules.customer.models.customer import Customer

    new_customer = Customer(
        email=email,
        full_name=full_name,
        phone=phone,
        status="active",
    )
    created = await customer_repo.create(new_customer)
    return uuid.UUID(str(created.id))


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    status_code=status.HTTP_201_CREATED,
)
async def checkout(payload: CheckoutRequest, db: AsyncSession = Depends(get_db)) -> Any:
    customer_id = await get_or_create_customer(
        db,
        email=payload.email,
        full_name=payload.full_name,
        phone=payload.phone,
    )

    shipping_address_dict = payload.shipping_address.model_dump()
    shipping_address_dict["full_name"] = payload.full_name
    if payload.phone:
        shipping_address_dict["phone"] = payload.phone

    order_create = OrderCreate(
        customer_id=customer_id,
        items=[item.model_dump() for item in payload.items],
        shipping_address=shipping_address_dict,
        currency=payload.currency,
        status="pending",
    )

    order_service = OrderService(db)
    try:
        order = await order_service.create(
            customer_id=order_create.customer_id,
            items=order_create.items,
            shipping_address=order_create.shipping_address,
            billing_address=order_create.billing_address,
            currency=order_create.currency,
            status=order_create.status,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc

    return CheckoutResponse(
        order_number=order.order_number,
        order_id=order.id,
        status=order.status,
        total_amount=order.total_amount,
        currency=order.currency,
    )
