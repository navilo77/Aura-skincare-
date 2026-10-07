from app.config.settings import settings

if settings.enable_email:
    from app.integrations.email.sendgrid import SendGridClient, sendgrid_client
else:
    from app.integrations.email.sendgrid import SendGridClient

    sendgrid_client = None

__all__ = ["SendGridClient", "sendgrid_client"]
