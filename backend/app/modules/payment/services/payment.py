import uuid
from decimal import Decimal
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.payment import stripe_client
from app.modules.payment.models import PaymentMethod, Refund
from app.modules.payment.repositories.payment import (
    PaymentMethodRepository,
    PaymentRepository,
    RefundRepository,
)
from app.modules.payment.schemas.payment import (
    PaymentCapture,
    PaymentConfirm,
    PaymentCreate,
    PaymentMethodCreate,
    PaymentMethodUpdate,
    PaymentRefund,
)


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.payment_repo = PaymentRepository(session)
        self.payment_method_repo = PaymentMethodRepository(session)
        self.refund_repo = RefundRepository(session)
        self.session = session

    def _require_stripe(self):
        if stripe_client is None:
            raise RuntimeError("Payment provider is disabled")

    async def create_payment_intent(
        self, payload: PaymentCreate, customer_stripe_id: str | None = None
    ) -> dict[str, Any]:
        self._require_stripe()
        stripe_pi = stripe_client.create_payment_intent(
            amount=payload.amount,
            currency=payload.currency,
            customer_id=customer_stripe_id,
            payment_method_id=payload.payment_method_id,
            description=payload.description,
            metadata=payload.metadata,
        )

        payment = await self.payment_repo.create(
            order_id=payload.order_id,
            customer_id=payload.customer_id,
            amount=payload.amount,
            currency=payload.currency,
            status=stripe_pi["status"],
            stripe_payment_intent_id=stripe_pi["id"],
            stripe_payment_method_id=payload.payment_method_id,
            description=payload.description,
            metadata=payload.metadata,
        )
        await self.session.flush()

        return {
            "client_secret": stripe_pi["client_secret"],
            "payment_intent_id": stripe_pi["id"],
            "status": stripe_pi["status"],
            "amount": payload.amount,
            "currency": payload.currency,
            "payment": payment,
        }

    async def confirm_payment(
        self, payment_intent_id: str, payload: PaymentConfirm
    ) -> dict[str, Any]:
        self._require_stripe()
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(
            payment_intent_id
        )
        if not payment:
            raise ValueError("Payment not found")

        stripe_pi = stripe_client.confirm_payment_intent(
            payment_intent_id=payment_intent_id,
            payment_method_id=payload.payment_method_id,
            return_url=payload.return_url,
        )

        payment.status = stripe_pi["status"]
        payment.stripe_payment_method_id = payload.payment_method_id
        if stripe_pi["status"] == "succeeded":
            from datetime import datetime

            payment.captured_at = datetime.utcnow()
        elif stripe_pi["status"] == "canceled":
            from datetime import datetime

            payment.failed_at = datetime.utcnow()
            payment.failure_reason = "Payment canceled"

        await self.session.flush()

        return {
            "client_secret": stripe_pi.get("client_secret"),
            "payment_intent_id": stripe_pi["id"],
            "status": stripe_pi["status"],
            "amount": payment.amount,
            "currency": payment.currency,
        }

    async def capture_payment(
        self, payment_intent_id: str, payload: PaymentCapture
    ) -> dict[str, Any]:
        self._require_stripe()
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(
            payment_intent_id
        )
        if not payment:
            raise ValueError("Payment not found")

        amount_to_capture = (
            int(payload.amount_to_capture * 100) if payload.amount_to_capture else None
        )
        stripe_pi = stripe_client.capture_payment_intent(
            payment_intent_id, amount_to_capture
        )

        payment.status = stripe_pi["status"]
        if stripe_pi["status"] == "succeeded":
            from datetime import datetime

            payment.captured_at = datetime.utcnow()
            if payload.amount_to_capture:
                payment.amount = Decimal(str(payload.amount_to_capture))

        await self.session.flush()

        return {
            "payment_intent_id": stripe_pi["id"],
            "status": stripe_pi["status"],
            "amount": payment.amount,
            "currency": payment.currency,
        }

    async def cancel_payment(self, payment_intent_id: str) -> dict[str, Any]:
        self._require_stripe()
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(
            payment_intent_id
        )
        if not payment:
            raise ValueError("Payment not found")

        stripe_pi = stripe_client.cancel_payment_intent(payment_intent_id)

        payment.status = stripe_pi["status"]
        from datetime import datetime

        payment.failed_at = datetime.utcnow()
        payment.failure_reason = "Payment canceled by user"

        await self.session.flush()

        return {"status": stripe_pi["status"]}

    async def create_refund(
        self, payment_intent_id: str, payload: PaymentRefund
    ) -> Refund:
        self._require_stripe()
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(
            payment_intent_id
        )
        if not payment:
            raise ValueError("Payment not found")

        amount_cents = int(payload.amount * 100) if payload.amount else None
        stripe_refund = stripe_client.create_refund(
            payment_intent_id=payment_intent_id,
            amount=amount_cents,
            reason=payload.reason,
            metadata=payload.metadata,
        )

        refund = await self.refund_repo.create(
            payment_id=payment.id,
            amount=payload.amount or payment.amount,
            currency=payment.currency,
            status=stripe_refund["status"],
            stripe_refund_id=stripe_refund["id"],
            reason=payload.reason,
            description=payload.description,
            metadata=payload.metadata,
        )

        if stripe_refund["status"] == "succeeded":
            from datetime import datetime

            refund.processed_at = datetime.utcnow()

        await self.session.flush()
        return refund

    async def handle_webhook(self, event_type: str, event_data: dict) -> dict[str, Any]:
        if event_type == "payment_intent.succeeded":
            await self._handle_payment_succeeded(event_data)
        elif event_type == "payment_intent.payment_failed":
            await self._handle_payment_failed(event_data)
        elif event_type == "payment_intent.canceled":
            await self._handle_payment_canceled(event_data)
        elif event_type == "charge.refunded":
            await self._handle_refund_succeeded(event_data)
        elif event_type == "refund.failed":
            await self._handle_refund_failed(event_data)

        return {"status": "processed"}

    async def _handle_payment_succeeded(self, event_data: dict) -> None:
        pi = event_data["object"]
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(pi["id"])
        if payment:
            payment.status = "succeeded"
            payment.stripe_charge_id = pi.get("latest_charge")
            from datetime import datetime

            payment.captured_at = datetime.utcnow()
            await self.session.flush()

    async def _handle_payment_failed(self, event_data: dict) -> None:
        pi = event_data["object"]
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(pi["id"])
        if payment:
            payment.status = "canceled"
            from datetime import datetime

            payment.failed_at = datetime.utcnow()
            payment.failure_reason = pi.get("last_payment_error", {}).get(
                "message", "Payment failed"
            )
            await self.session.flush()

    async def _handle_payment_canceled(self, event_data: dict) -> None:
        pi = event_data["object"]
        payment = await self.payment_repo.get_by_stripe_payment_intent_id(pi["id"])
        if payment:
            payment.status = "canceled"
            from datetime import datetime

            payment.failed_at = datetime.utcnow()
            payment.failure_reason = "Payment canceled"
            await self.session.flush()

    async def _handle_refund_succeeded(self, event_data: dict) -> None:
        refund_obj = event_data["object"]
        refund = await self.refund_repo.get_by_stripe_refund_id(refund_obj["id"])
        if refund:
            refund.status = "succeeded"
            from datetime import datetime

            refund.processed_at = datetime.utcnow()
            await self.session.flush()

    async def _handle_refund_failed(self, event_data: dict) -> None:
        refund_obj = event_data["object"]
        refund = await self.refund_repo.get_by_stripe_refund_id(refund_obj["id"])
        if refund:
            refund.status = "failed"
            await self.session.flush()


class PaymentMethodService:
    def __init__(self, session: AsyncSession):
        self.payment_method_repo = PaymentMethodRepository(session)
        self.session = session

    async def create_payment_method(
        self, payload: PaymentMethodCreate, customer_stripe_id: str
    ) -> PaymentMethod:
        if stripe_client is None:
            raise RuntimeError("Payment provider is disabled")
        stripe_pm = stripe_client.attach_payment_method(
            payload.stripe_payment_method_id, customer_stripe_id
        )

        card = stripe_pm.get("card", {})
        payment_method = await self.payment_method_repo.create(
            customer_id=payload.customer_id,
            type=payload.type,
            stripe_payment_method_id=payload.stripe_payment_method_id,
            card_brand=card.get("brand"),
            card_last4=card.get("last4"),
            card_exp_month=card.get("exp_month"),
            card_exp_year=card.get("exp_year"),
            is_default=payload.is_default,
            metadata=payload.metadata,
        )

        if payload.is_default:
            await self.payment_method_repo.set_default(
                payload.customer_id, payment_method.id
            )

        await self.session.flush()
        return payment_method

    async def list_payment_methods(
        self, customer_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[PaymentMethod], int]:
        return await self.payment_method_repo.get_by_customer_id(
            customer_id, skip, limit
        )

    async def get_default(self, customer_id: uuid.UUID) -> PaymentMethod | None:
        return await self.payment_method_repo.get_default(customer_id)

    async def update_payment_method(
        self, payment_method_id: uuid.UUID, payload: PaymentMethodUpdate
    ) -> PaymentMethod | None:
        payment_method = await self.payment_method_repo.get_by_id(payment_method_id)
        if not payment_method:
            return None

        if payload.is_default is not None:
            payment_method.is_default = payload.is_default
            if payload.is_default:
                await self.payment_method_repo.set_default(
                    payment_method.customer_id, payment_method_id
                )

        if payload.metadata is not None:
            payment_method.metadata = payload.metadata

        await self.session.flush()
        return payment_method

    async def delete_payment_method(self, payment_method_id: uuid.UUID) -> bool:
        if stripe_client is None:
            raise RuntimeError("Payment provider is disabled")
        payment_method = await self.payment_method_repo.get_by_id(payment_method_id)
        if not payment_method:
            return False

        stripe_client.detach_payment_method(payment_method.stripe_payment_method_id)
        return await self.payment_method_repo.delete(payment_method_id)
