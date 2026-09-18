import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import Permission, Role
from app.modules.auth.schemas.role import (
    PermissionCreate,
    PermissionRead,
    RoleCreate,
    RoleRead,
    RoleUpdate,
)
from app.modules.auth.services.role import PermissionService, RoleService
from app.shared.database.session import get_db

router = APIRouter(tags=["roles"])


@router.get("/roles", response_model=list[RoleRead])
async def list_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = RoleService(db)
    roles, _ = await service.get_list(skip=skip, limit=limit)
    return roles


@router.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(payload: RoleCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = RoleService(db)
    try:
        role = await service.create(
            name=payload.name,
            description=payload.description,
            permission_ids=payload.permission_ids,
        )
        return role
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/roles/{role_id}", response_model=RoleRead)
async def get_role(role_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = RoleService(db)
    role = await service.get_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role


@router.patch("/roles/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: uuid.UUID, payload: RoleUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = RoleService(db)
    try:
        role = await service.update(
            role_id=role_id,
            name=payload.name,
            description=payload.description,
            permission_ids=payload.permission_ids,
        )
        return role
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_role(role_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    service = RoleService(db)
    try:
        await service.delete(role_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/permissions", response_model=list[PermissionRead])
async def list_permissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = PermissionService(db)
    permissions, _ = await service.get_list(skip=skip, limit=limit)
    return permissions


@router.post(
    "/permissions", response_model=PermissionRead, status_code=status.HTTP_201_CREATED
)
async def create_permission(
    payload: PermissionCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = PermissionService(db)
    try:
        permission = await service.create(
            name=payload.name,
            description=payload.description,
        )
        return permission
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
