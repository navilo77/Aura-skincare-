import os
from decimal import Decimal
from typing import Any

from app.config.settings import settings

if settings.enable_payment:
    import stripe

    class StripeClient:
        def __init__(self):
            self.client = stripe.StripeClient(
                settings.stripe_secret_key or os.getenv("STRIPE_SECRET_KEY", "")
            )

        def create_payment_intent(
            self,
            amount: Decimal,
            currency: str,
            customer_id: str | None = None,
            payment_method_id: str | None = None,
            description: str | None = None,
            metadata: dict | None = None,
            capture_method: str = "automatic",
            confirm: bool = False,
        ) -> dict[str, Any]:
            params = {
                "amount": int(amount * 100),
                "currency": currency.lower(),
                "capture_method": capture_method,
                "confirm": confirm,
            }
            if customer_id:
                params["customer"] = customer_id
            if payment_method_id:
                params["payment_method"] = payment_method_id
            if description:
                params["description"] = description
            if metadata:
                params["metadata"] = metadata

            return self.client.payment_intents.create(**params)

        def confirm_payment_intent(
            self,
            payment_intent_id: str,
            payment_method_id: str,
            return_url: str | None = None,
        ) -> dict[str, Any]:
            params = {"payment_method": payment_method_id}
            if return_url:
                params["return_url"] = return_url
            return self.client.payment_intents.confirm(payment_intent_id, **params)

        def capture_payment_intent(
            self,
            payment_intent_id: str,
            amount_to_capture: int | None = None,
        ) -> dict[str, Any]:
            params = {}
            if amount_to_capture:
                params["amount_to_capture"] = amount_to_capture
            return self.client.payment_intents.capture(payment_intent_id, **params)

        def cancel_payment_intent(self, payment_intent_id: str) -> dict[str, Any]:
            return self.client.payment_intents.cancel(payment_intent_id)

        def create_refund(
            self,
            payment_intent_id: str,
            amount: int | None = None,
            reason: str | None = None,
            metadata: dict | None = None,
        ) -> dict[str, Any]:
            params = {"payment_intent": payment_intent_id}
            if amount:
                params["amount"] = amount
            if reason:
                params["reason"] = reason
            if metadata:
                params["metadata"] = metadata
            return self.client.refunds.create(**params)

        def create_customer(
            self, email: str, name: str | None = None, metadata: dict | None = None
        ) -> dict[str, Any]:
            params = {"email": email}
            if name:
                params["name"] = name
            if metadata:
                params["metadata"] = metadata
            return self.client.customers.create(**params)

        def attach_payment_method(
            self, payment_method_id: str, customer_id: str
        ) -> dict[str, Any]:
            return self.client.payment_methods.attach(
                payment_method_id, customer=customer_id
            )

        def detach_payment_method(self, payment_method_id: str) -> dict[str, Any]:
            return self.client.payment_methods.detach(payment_method_id)

        def list_payment_methods(
            self, customer_id: str, type: str = "card"
        ) -> dict[str, Any]:
            return self.client.payment_methods.list(customer=customer_id, type=type)

        def construct_webhook_event(
            self, payload: bytes, sig_header: str, webhook_secret: str
        ) -> dict[str, Any]:
            return stripe.Webhook.construct_event(payload, sig_header, webhook_secret)

    stripe_client = StripeClient()
else:

    class StripeClient:
        pass

    stripe_client = None
