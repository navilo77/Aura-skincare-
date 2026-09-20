from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.auth.models.user import User
from app.modules.auth.repositories.user import UserRepository
from app.modules.auth.services.auth import AuthService
from app.modules.customer.models.address import Address
from app.modules.customer.models.customer import Customer
from app.modules.customer.repositories.customer import CustomerRepository
from app.shared.database.session import get_db
from app.shared.security.password import hash_password, verify_password

router = APIRouter(tags=["profile"])


class ProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class AddressBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=2, max_length=2)
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address_line1: str | None = Field(None, min_length=1, max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    city: str | None = Field(None, min_length=1, max_length=100)
    state: str | None = Field(None, min_length=1, max_length=100)
    postal_code: str | None = Field(None, min_length=1, max_length=20)
    country: str | None = Field(None, min_length=2, max_length=2)
    is_default: bool | None = None


class AddressRead(AddressBase):
    id: uuid.UUID
    customer_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


@router.get("", response_model=ProfileRead)
async def get_profile(
    current_user: User = Depends(get_current_user),
) -> ProfileRead:
    return ProfileRead.model_validate(current_user)


@router.patch("", response_model=ProfileRead)
async def update_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProfileRead:
    user_repository = UserRepository(db)
    user = await user_repository.get_by_id(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if payload.full_name is not None:
        user.full_name = payload.full_name.strip()
    if payload.email is not None:
        email = payload.email.strip().lower()
        existing = await user_repository.get_by_email(email)
        if existing and existing.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already in use"
            )
        user.email = email

    await db.flush()
    await db.refresh(user)
    return ProfileRead.model_validate(user)


@router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def change_password(
    payload: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    user_repository = UserRepository(db)
    user = await user_repository.get_by_id(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.password_hash = hash_password(payload.new_password)
    await db.flush()


@router.post(
    "/forgot-password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def forgot_password(
    payload: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
) -> None:
    user_repository = UserRepository(db)
    user = await user_repository.get_by_email(payload.email.strip().lower())
    if not user:
        return None

    token_service = AuthService(db).token_service
    token = token_service.create_access_token(user.id, user.role)
    expires_at = datetime.now(UTC) + timedelta(hours=1)

    from app.modules.auth.models.password_reset_token import PasswordResetToken
    from app.modules.auth.repositories.password_reset_token import (
        PasswordResetTokenRepository,
    )

    token_repository = PasswordResetTokenRepository(db)
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
    )
    token_repository.session.add(reset_token)
    await token_repository.session.flush()
    return None


@router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def reset_password(
    payload: PasswordReset,
    db: AsyncSession = Depends(get_db),
) -> None:
    from app.modules.auth.repositories.password_reset_token import (
        PasswordResetTokenRepository,
    )

    token_repository = PasswordResetTokenRepository(db)
    reset_token = await token_repository.get_by_token(payload.token)
    if not reset_token or reset_token.expires_at < datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )
    user_repository = UserRepository(db)
    user = await user_repository.get_by_id(reset_token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.password_hash = hash_password(payload.new_password)
    reset_token.used_at = datetime.now(UTC)
    await db.flush()


@router.get("/addresses", response_model=list[AddressRead])
async def list_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[AddressRead]:
    customer_repository = CustomerRepository(db)
    customer = await customer_repository.get_by_email(current_user.email)
    if not customer:
        return []
    return [AddressRead.model_validate(address) for address in customer.addresses]


@router.post(
    "/addresses", response_model=AddressRead, status_code=status.HTTP_201_CREATED
)
async def create_address(
    payload: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AddressRead:
    customer_repository = CustomerRepository(db)
    customer = await customer_repository.get_by_email(current_user.email)
    if not customer:
        customer = Customer(
            full_name=current_user.full_name,
            email=current_user.email,
            phone=None,
            status="active",
        )
        db.add(customer)
        await db.flush()
        await db.refresh(customer)
    address = Address(
        customer_id=customer.id,
        address_line1=payload.address_line1,
        address_line2=payload.address_line2,
        city=payload.city,
        state=payload.state,
        postal_code=payload.postal_code,
        country=payload.country,
        is_default=payload.is_default,
    )
    db.add(address)
    await db.flush()
    await db.refresh(address)
    return AddressRead.model_validate(address)


@router.patch("/addresses/{address_id}", response_model=AddressRead)
async def update_address(
    address_id: uuid.UUID,
    payload: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AddressRead:
    customer_repository = CustomerRepository(db)
    customer = await customer_repository.get_by_email(current_user.email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    address = next((a for a in customer.addresses if a.id == address_id), None)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    if payload.address_line1 is not None:
        address.address_line1 = payload.address_line1
    if payload.address_line2 is not None:
        address.address_line2 = payload.address_line2
    if payload.city is not None:
        address.city = payload.city
    if payload.state is not None:
        address.state = payload.state
    if payload.postal_code is not None:
        address.postal_code = payload.postal_code
    if payload.country is not None:
        address.country = payload.country
    if payload.is_default is not None:
        address.is_default = payload.is_default
    await db.flush()
    await db.refresh(address)
    return AddressRead.model_validate(address)


@router.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_address(
    address_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    customer_repository = CustomerRepository(db)
    customer = await customer_repository.get_by_email(current_user.email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    address = next((a for a in customer.addresses if a.id == address_id), None)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    await db.delete(address)
    await db.flush()
