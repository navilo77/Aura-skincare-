from app.config.settings import settings

if settings.enable_payment:
    from app.integrations.payment.stripe import StripeClient, stripe_client
else:
    from app.integrations.payment.stripe import StripeClient

    stripe_client = None

__all__ = ["StripeClient", "stripe_client"]
