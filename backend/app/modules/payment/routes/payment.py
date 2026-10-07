import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.config.settings import settings
from app.integrations.payment import stripe_client
from app.modules.auth.models.user import User
from app.modules.payment.schemas.payment import (
    PaymentCapture,
    PaymentConfirm,
    PaymentCreate,
    PaymentIntentResponse,
    PaymentList,
    PaymentMethodCreate,
    PaymentMethodRead,
    PaymentMethodUpdate,
    PaymentRead,
    PaymentRefund,
    RefundRead,
)
from app.modules.payment.services.payment import PaymentMethodService, PaymentService
from app.shared.database.session import get_db

router = APIRouter(tags=["payments"])


@router.post(
    "/intent", response_model=PaymentIntentResponse, status_code=status.HTTP_201_CREATED
)
async def create_payment_intent(
    payload: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    if stripe_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment provider is disabled",
        )
    service = PaymentService(db)
    customer_stripe_id = getattr(current_user, "stripe_customer_id", None)
    result = await service.create_payment_intent(payload, customer_stripe_id)
    return result


@router.post("/{payment_intent_id}/confirm", response_model=PaymentIntentResponse)
async def confirm_payment(
    payment_intent_id: str,
    payload: PaymentConfirm,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentService(db)
    result = await service.confirm_payment(payment_intent_id, payload)
    return result


@router.post("/{payment_intent_id}/capture", response_model=PaymentIntentResponse)
async def capture_payment(
    payment_intent_id: str,
    payload: PaymentCapture,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentService(db)
    result = await service.capture_payment(payment_intent_id, payload)
    return result


@router.post("/{payment_intent_id}/cancel")
async def cancel_payment(
    payment_intent_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentService(db)
    result = await service.cancel_payment(payment_intent_id)
    return result


@router.post(
    "/{payment_intent_id}/refund",
    response_model=RefundRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_refund(
    payment_intent_id: str,
    payload: PaymentRefund,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentService(db)
    refund = await service.create_refund(payment_intent_id, payload)
    return RefundRead.model_validate(refund)


@router.get("", response_model=list[PaymentList])
async def list_payments(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentService(db)
    payments, _ = await service.payment_repo.get_by_customer_id(
        current_user.id, skip, limit
    )
    return [PaymentList.model_validate(p) for p in payments]


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(
    payment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentService(db)
    payment = await service.payment_repo.get_by_id(payment_id)
    if not payment or payment.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    return PaymentRead.model_validate(payment)


@router.post(
    "/methods", response_model=PaymentMethodRead, status_code=status.HTTP_201_CREATED
)
async def create_payment_method(
    payload: PaymentMethodCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentMethodService(db)
    customer_stripe_id = getattr(current_user, "stripe_customer_id", None)
    if not customer_stripe_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer not linked to Stripe",
        )
    payment_method = await service.create_payment_method(payload, customer_stripe_id)
    return PaymentMethodRead.model_validate(payment_method)


@router.get("/methods", response_model=list[PaymentMethodRead])
async def list_payment_methods(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentMethodService(db)
    methods, _ = await service.list_payment_methods(current_user.id, skip, limit)
    return [PaymentMethodRead.model_validate(m) for m in methods]


@router.get("/methods/default", response_model=PaymentMethodRead)
async def get_default_payment_method(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentMethodService(db)
    method = await service.get_default(current_user.id)
    if not method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No default payment method"
        )
    return PaymentMethodRead.model_validate(method)


@router.patch("/methods/{method_id}", response_model=PaymentMethodRead)
async def update_payment_method(
    method_id: uuid.UUID,
    payload: PaymentMethodUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PaymentMethodService(db)
    method = await service.update_payment_method(method_id, payload)
    if not method or method.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found"
        )
    return PaymentMethodRead.model_validate(method)


@router.delete(
    "/methods/{method_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_payment_method(
    method_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    service = PaymentMethodService(db)
    method = await service.payment_method_repo.get_by_id(method_id)
    if not method or method.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found"
        )
    success = await service.delete_payment_method(method_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete payment method",
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Any:
    if stripe_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment provider is disabled",
        )
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = settings.stripe_webhook_secret or ""

    if not sig_header or not webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing signature or webhook secret",
        )

    try:
        event = stripe_client.construct_webhook_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid webhook signature: {str(e)}",
        )

    service = PaymentService(db)
    await service.handle_webhook(event["type"], event["data"])

    return {"status": "success"}
