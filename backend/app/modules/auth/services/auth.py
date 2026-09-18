import uuid

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.auth.repositories.user import UserRepository
from app.modules.auth.services.token import TokenService
from app.shared.security.jwt import decode_token
from app.shared.security.password import hash_password, verify_password
from typing import Any



class AuthService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.token_service = TokenService(session)

    async def register(
        self, email: str, password: str, full_name: str, role: str = "customer"
    ) -> Any:
        if await self.repository.exists_by_email(email):
            raise ValueError("Email already registered")

        user = User(
            email=email.lower(),
            password_hash=hash_password(password),
            full_name=full_name,
            role=role,
            is_active=True,
            is_verified=False,
        )
        return await self.repository.create(user)

    async def login(self, email: str, password: str) -> Any:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is inactive")

        access_token = self.token_service.create_access_token(user.id, user.role)
        refresh_token = self.token_service.create_refresh_token(user.id)

        payload = decode_token(refresh_token)
        if payload is None:
            raise ValueError("Invalid refresh token")
        jti = payload.get("jti")
        exp_val = payload.get("exp")
        if exp_val is None:
            raise ValueError("Invalid refresh token")
        exp = datetime.fromtimestamp(exp_val, tz=UTC)

        await self.token_service.create_refresh_token_record(user.id, str(jti), exp)

        user.last_login_at = datetime.now(UTC)
        await self.repository.session.flush()

        return user, access_token, refresh_token

    async def refresh(self, refresh_token: str) -> Any:
        try:
            payload = decode_token(refresh_token)
        except Exception as exc:
            raise ValueError("Invalid refresh token") from exc

        if payload is None:
            raise ValueError("Invalid refresh token")
        jti = payload.get("jti")
        user_id_val = payload.get("sub")
        if jti is None or user_id_val is None:
            raise ValueError("Invalid refresh token")
        user_id = uuid.UUID(user_id_val)
        token_record = await self.token_service.refresh_repository.get_by_jti(jti)
        if (
            not token_record
            or token_record.is_revoked
            or token_record.expires_at < datetime.now(UTC)
        ):
            raise ValueError("Invalid or expired refresh token")

        user = await self.repository.get_by_id(uuid.UUID(str(user_id)))
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        new_access = self.token_service.create_access_token(user.id, user.role)
        new_refresh = self.token_service.create_refresh_token(user.id)

        new_payload = decode_token(new_refresh)
        if new_payload is None:
            raise ValueError("Invalid refresh token")
        if new_payload is None:
            raise ValueError("Invalid refresh token")
        new_jti = new_payload.get("jti")
        new_exp_val = new_payload.get("exp")
        if new_exp_val is None:
            raise ValueError("Invalid refresh token")
        new_exp = datetime.fromtimestamp(new_exp_val, tz=UTC)

        await self.token_service.create_refresh_token_record(user.id, str(new_jti), new_exp)
        await self.token_service.revoke_refresh_token(jti)

        return new_access, new_refresh

    async def get_by_id(self, user_id: uuid.UUID) -> Any:
        return await self.repository.get_by_id(user_id)
