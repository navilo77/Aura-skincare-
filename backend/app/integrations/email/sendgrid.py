import os
from typing import Any

from app.config.settings import settings

if settings.enable_email:
    import sendgrid
    from sendgrid.helpers.mail import Content, Email, Mail, To

    class SendGridClient:
        def __init__(self):
            self.api_key = settings.sendgrid_api_key or os.getenv(
                "SENDGRID_API_KEY", ""
            )
            self.client = (
                sendgrid.SendGridAPIClient(api_key=self.api_key)
                if self.api_key
                else None
            )
            self.from_email = settings.sendgrid_from_email or os.getenv(
                "SENDGRID_FROM_EMAIL", "noreply@auraskincare.com"
            )
            self.from_name = settings.sendgrid_from_name or os.getenv(
                "SENDGRID_FROM_NAME", "Aura Skincare"
            )

        def send_email(
            self,
            to_email: str,
            subject: str,
            html_content: str,
            text_content: str | None = None,
            from_email: str | None = None,
            from_name: str | None = None,
        ) -> dict[str, Any]:
            if not self.client:
                return {"success": False, "error": "SendGrid not configured"}

            try:
                mail = Mail(
                    from_email=Email(
                        from_email or self.from_email, from_name or self.from_name
                    ),
                    to_emails=To(to_email),
                    subject=subject,
                    html_content=Content("text/html", html_content),
                )
                if text_content:
                    mail.content = [
                        Content("text/plain", text_content),
                        Content("text/html", html_content),
                    ]

                response = self.client.send(mail)
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "message_id": response.headers.get("X-Message-Id"),
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        def send_template_email(
            self,
            to_email: str,
            template_id: str,
            dynamic_template_data: dict[str, Any],
            from_email: str | None = None,
            from_name: str | None = None,
        ) -> dict[str, Any]:
            if not self.client:
                return {"success": False, "error": "SendGrid not configured"}

            try:
                mail = Mail(
                    from_email=Email(
                        from_email or self.from_email, from_name or self.from_name
                    ),
                    to_emails=To(to_email),
                )
                mail.template_id = template_id
                mail.dynamic_template_data = dynamic_template_data

                response = self.client.send(mail)
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "message_id": response.headers.get("X-Message-Id"),
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

    sendgrid_client = SendGridClient()
else:

    class SendGridClient:
        pass

    sendgrid_client = None
