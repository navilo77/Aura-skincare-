import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.schemas.user import (
    LoginRequest,
    RefreshRequest,
    Token,
    UserCreate,
    UserRead,
)
from app.modules.auth.services.auth import AuthService
from app.shared.database.session import get_db

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    try:
        user = await service.register(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            role=payload.role,
        )
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    try:
        user, access_token, refresh_token = await service.login(
            email=payload.email,
            password=payload.password,
        )
        return Token(access_token=access_token, refresh_token=refresh_token)
    except ValueError as exc:
        error_message = str(exc)
        if error_message == "Account is inactive":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=error_message
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message
        ) from exc


@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    try:
        access_token, refresh_token = await service.refresh(payload.refresh_token)
        return Token(access_token=access_token, refresh_token=refresh_token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def logout(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    try:
        await service.token_service.revoke_refresh_token(payload.refresh_token)
    except Exception:
        pass
    return None


@router.get("/me", response_model=UserRead)
async def get_me(user_id: str, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    user = await service.get_by_id(uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
