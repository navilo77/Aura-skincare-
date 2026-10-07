import json
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.modules.admin.models.audit_log import AuditLog
from app.modules.auth.models.user import User
from app.shared.database.session import get_db


class AuditLogMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        excluded_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.excluded_paths = excluded_paths or [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
        ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        if request.method in (
            "GET",
            "HEAD",
            "OPTIONS",
        ) and not request.url.path.startswith("/api/v1/admin"):
            return await call_next(request)

        user: User | None = getattr(request.state, "user", None)

        request_body = await self._get_request_body(request)

        response = await call_next(request)

        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            await self._log_audit(
                request=request,
                user=user,
                request_body=request_body,
                response_status=response.status_code,
            )

        return response

    async def _get_request_body(self, request: Request) -> dict | None:
        try:
            if request.method in ("POST", "PUT", "PATCH"):
                body = await request.body()
                if body:
                    return json.loads(body.decode())
        except Exception:
            pass
        return None

    async def _log_audit(
        self,
        request: Request,
        user: User | None,
        request_body: dict | None,
        response_status: int,
    ) -> None:
        try:
            path_parts = request.url.path.strip("/").split("/")
            entity_type = path_parts[-2] if len(path_parts) >= 2 else "unknown"
            entity_id = None

            if len(path_parts) >= 3:
                try:
                    entity_id = uuid.UUID(path_parts[-1])
                except ValueError:
                    pass

            audit_log = AuditLog(
                user_id=user.id if user else None,
                action=f"{request.method} {request.url.path}",
                entity_type=entity_type,
                entity_id=entity_id,
                old_values=None,
                new_values=json.dumps(request_body) if request_body else None,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
            )

            async with get_db() as db:
                db.add(audit_log)
                await db.commit()

        except Exception:
            pass
