from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import EmailVerification
from app.modules.auth.repositories.email_verification import EmailVerificationRepository
from app.modules.auth.services.auth import AuthService
from app.shared.database.session import get_db

router = APIRouter(tags=["auth"])


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(
    token: str = Query(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    repository = EmailVerificationRepository(db)
    verification = await repository.get_by_token(token)
    if not verification or verification.expires_at < datetime.now(UTC).replace(tzinfo=None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )
    service = AuthService(db)
    user = await service.get_by_id(verification.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.is_verified = True
    verification.verified_at = datetime.now(UTC).replace(tzinfo=None)
    await db.flush()
    return {"message": "Email verified successfully"}


@router.post("/resend-verification", status_code=status.HTTP_200_OK)
async def resend_verification(
    email: str = Query(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    service = AuthService(db)
    user = await service.repository.get_by_email(email.strip().lower())
    if not user:
        return {"message": "If an account exists, a verification email has been sent"}
    if user.is_verified:
        return {"message": "Email already verified"}

    token = service.token_service.create_access_token(
        user.id, user.role
    )
    expires_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(hours=24)

    verification = EmailVerification(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
    )
    db.add(verification)
    await db.flush()
    return {"message": "Verification email sent"}
