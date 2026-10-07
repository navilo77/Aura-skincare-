import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.auth.models.user import User
from app.modules.notification.schemas.notification import (
    PreferenceCreate,
    PreferenceRead,
    PreferenceUpdate,
)
from app.modules.notification.services.preference import PreferenceService
from app.shared.database.session import get_db

router = APIRouter(tags=["notification-preferences"])


@router.get("", response_model=list[PreferenceRead])
async def list_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PreferenceService(db)
    preferences = await service.get_by_user(current_user.id)
    return [PreferenceRead.model_validate(p) for p in preferences]


@router.post("", response_model=PreferenceRead, status_code=status.HTTP_201_CREATED)
async def create_preference(
    payload: PreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PreferenceService(db)
    payload.user_id = current_user.id
    preference = await service.create(**payload.model_dump())
    return PreferenceRead.model_validate(preference)


@router.patch("/{preference_id}", response_model=PreferenceRead)
async def update_preference(
    preference_id: uuid.UUID,
    payload: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PreferenceService(db)
    preference = await service.update(
        preference_id, **payload.model_dump(exclude_unset=True)
    )
    if not preference or preference.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preference not found"
        )
    return PreferenceRead.model_validate(preference)


@router.get("/{preference_id}", response_model=PreferenceRead)
async def get_preference(
    preference_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PreferenceService(db)
    preference = await service.get_by_id(preference_id)
    if not preference or preference.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preference not found"
        )
    return PreferenceRead.model_validate(preference)


@router.delete(
    "/{preference_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_preference(
    preference_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PreferenceService(db)
    preference = await service.get_by_id(preference_id)
    if not preference or preference.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preference not found"
        )
    await service.delete(preference_id)
