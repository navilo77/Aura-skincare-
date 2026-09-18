import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import Permission, Role
from app.modules.auth.repositories.role import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
)


class RoleService:
    def __init__(self, session: AsyncSession):
        self.repository = RoleRepository(session)
        self.permission_repository = PermissionRepository(session)
        self.role_permission_repository = RolePermissionRepository(session)

    async def create(
        self,
        name: str,
        description: str | None = None,
        permission_ids: list[uuid.UUID] | None = None,
    ) -> Any:
        if await self.repository.exists_by_name(name):
            raise ValueError("Role name already exists")

        role = Role(name=name, description=description)
        await self.repository.create(role)

        if permission_ids:
            for permission_id in permission_ids:
                await self.role_permission_repository.create_link(
                role.id, permission_id
            )

        return role

    async def update(
        self,
        role_id: uuid.UUID,
        name: str | None = None,
        description: str | None = None,
        permission_ids: list[uuid.UUID] | None = None,
    ) -> Any:
        role = await self.repository.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")

        if name is not None:
            existing = await self.repository.get_by_name(name)
            if existing and existing.id != role_id:
                raise ValueError("Role name already exists")
            role.name = name

        if description is not None:
            role.description = description

        if permission_ids is not None:
            existing_links = await self.role_permission_repository.get_by_role(role_id)
            for link in existing_links:
                await self.repository.session.delete(link)
            await self.repository.session.flush()

            for permission_id in permission_ids:
                await self.role_permission_repository.create_link(
                role_id, permission_id
            )

        return role

    async def delete(self, role_id: uuid.UUID) -> Any:
        role = await self.repository.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        await self.repository.delete(role_id)

    async def get_by_id(self, role_id: uuid.UUID) -> Any:
        return await self.repository.get_by_id(role_id)

    async def get_list(self, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_list(skip=skip, limit=limit)


class PermissionService:
    def __init__(self, session: AsyncSession):
        self.repository = PermissionRepository(session)

    async def create(self, name: str, description: str | None = None) -> Any:
        if await self.repository.get_by_name(name):
            raise ValueError("Permission name already exists")

        permission = Permission(name=name, description=description)
        return await self.repository.create(permission)

    async def get_by_id(self, permission_id: uuid.UUID) -> Any:
        return await self.repository.get_by_id(permission_id)

    async def get_list(
        self, skip: int = 0, limit: int = 20
    ) -> Any:
        return await self.repository.get_list(skip=skip, limit=limit)
