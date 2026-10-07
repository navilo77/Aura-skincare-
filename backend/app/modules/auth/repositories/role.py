import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import Permission, Role, RolePermission
from app.modules.auth.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Permission)

    async def get_by_name(self, name: str) -> Permission | None:
        result = await self.session.execute(
            select(Permission).where(Permission.name == name)
        )
        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        result = await self.session.execute(
            select(Permission).where(Permission.name == name)
        )
        return result.scalar_one_or_none() is not None

    async def get_list(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[Permission], int]:
        query = select(Permission).order_by(Permission.name)
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total


class RoleRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Role)

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.session.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        result = await self.session.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none() is not None

    async def get_list(self, skip: int = 0, limit: int = 20) -> tuple[list[Role], int]:
        query = select(Role).order_by(Role.name)
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total


class RolePermissionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RolePermission)

    async def get_by_role(self, role_id: uuid.UUID) -> list[RolePermission]:
        result = await self.session.execute(
            select(RolePermission).where(RolePermission.role_id == role_id)
        )
        return list(result.scalars().all())

    async def get_by_permission(self, permission_id: uuid.UUID) -> list[RolePermission]:
        result = await self.session.execute(
            select(RolePermission).where(RolePermission.permission_id == permission_id)
        )
        return list(result.scalars().all())

    async def exists(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def create_link(
        self, role_id: uuid.UUID, permission_id: uuid.UUID
    ) -> RolePermission:
        link = RolePermission(role_id=role_id, permission_id=permission_id)
        return await self.create(link)  # type: ignore[no-any-return]
