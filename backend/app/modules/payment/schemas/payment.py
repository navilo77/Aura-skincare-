import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: uuid.UUID
    customer_id: uuid.UUID
    amount: Decimal = Field(..., gt=Decimal("0"))
    currency: str = Field("USD", min_length=3, max_length=3)
    description: str | None = None


class PaymentCreate(PaymentBase):
    payment_method_id: str | None = None
    metadata: dict | None = None


class PaymentConfirm(BaseModel):
    payment_method_id: str
    return_url: str | None = None


class PaymentCapture(BaseModel):
    amount_to_capture: Decimal | None = None


class PaymentRefund(BaseModel):
    amount: Decimal | None = None
    reason: str | None = Field(
        None, pattern="^(duplicate|fraudulent|requested_by_customer)$"
    )
    description: str | None = None
    metadata: dict | None = None


class PaymentRead(PaymentBase):
    id: uuid.UUID
    status: str
    stripe_payment_intent_id: str | None = None
    stripe_payment_method_id: str | None = None
    stripe_charge_id: str | None = None
    metadata: dict | None = None
    captured_at: datetime | None = None
    failed_at: datetime | None = None
    failure_reason: str | None = None
    created_at: datetime
    updated_at: datetime


class PaymentList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    customer_id: uuid.UUID
    amount: Decimal
    currency: str
    status: str
    stripe_payment_intent_id: str | None = None
    created_at: datetime


class PaymentMethodBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: uuid.UUID
    type: str = Field("card", pattern="^(card|bank_transfer|wallet)$")


class PaymentMethodCreate(PaymentMethodBase):
    stripe_payment_method_id: str
    card_brand: str | None = None
    card_last4: str | None = None
    card_exp_month: int | None = None
    card_exp_year: int | None = None
    is_default: bool = False
    metadata: dict | None = None


class PaymentMethodRead(PaymentMethodBase):
    id: uuid.UUID
    stripe_payment_method_id: str
    card_brand: str | None = None
    card_last4: str | None = None
    card_exp_month: int | None = None
    card_exp_year: int | None = None
    is_default: bool
    metadata: dict | None = None
    created_at: datetime
    updated_at: datetime


class PaymentMethodUpdate(BaseModel):
    is_default: bool | None = None
    metadata: dict | None = None


class RefundBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_id: uuid.UUID
    amount: Decimal = Field(..., gt=Decimal("0"))
    currency: str = Field("USD", min_length=3, max_length=3)


class RefundCreate(RefundBase):
    reason: str | None = Field(
        None, pattern="^(duplicate|fraudulent|requested_by_customer)$"
    )
    description: str | None = None
    metadata: dict | None = None


class RefundRead(RefundBase):
    id: uuid.UUID
    status: str
    stripe_refund_id: str | None = None
    reason: str | None = None
    description: str | None = None
    metadata: dict | None = None
    processed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str
    status: str
    amount: Decimal
    currency: str


class WebhookEvent(BaseModel):
    id: str
    type: str
    data: dict
    created: int
