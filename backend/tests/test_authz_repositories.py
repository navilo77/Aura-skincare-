import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import Permission, Role, RolePermission
from app.modules.auth.repositories.role import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
)


@pytest.mark.asyncio
async def test_permission_repository(db_session: AsyncSession):
    repo = PermissionRepository(db_session)
    permission = Permission(name="perm1", description="Permission 1")
    db_session.add(permission)
    await db_session.flush()

    fetched = await repo.get_by_id(permission.id)
    assert fetched is not None
    assert fetched.name == "perm1"

    by_name = await repo.get_by_name("perm1")
    assert by_name is not None

    await repo.delete(permission.id)
    assert await repo.get_by_id(permission.id) is None


@pytest.mark.asyncio
async def test_role_repository(db_session: AsyncSession):
    repo = RoleRepository(db_session)
    role = Role(name="role1", description="Role 1")
    db_session.add(role)
    await db_session.flush()

    fetched = await repo.get_by_id(role.id)
    assert fetched is not None
    assert fetched.name == "role1"

    by_name = await repo.get_by_name("role1")
    assert by_name is not None

    await repo.delete(role.id)
    assert await repo.get_by_id(role.id) is None


@pytest.mark.asyncio
async def test_role_permission_repository(db_session: AsyncSession):
    role = Role(name="role2", description="Role 2")
    db_session.add(role)
    await db_session.flush()

    permission = Permission(name="perm2", description="Permission 2")
    db_session.add(permission)
    await db_session.flush()

    link_repo = RolePermissionRepository(db_session)
    link = RolePermission(role_id=role.id, permission_id=permission.id)
    db_session.add(link)
    await db_session.flush()

    assert await link_repo.exists(role.id, permission.id) is True

    by_role = await link_repo.get_by_role(role.id)
    assert len(by_role) == 1

    await link_repo.delete(link.id)
    assert await link_repo.exists(role.id, permission.id) is False
