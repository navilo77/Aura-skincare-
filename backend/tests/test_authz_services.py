
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import RolePermission
from app.modules.auth.services.role import PermissionService, RoleService


@pytest.mark.asyncio
async def test_role_service_crud(db_session: AsyncSession):
    service = RoleService(db_session)
    role = await service.create(name="admin", description="Administrator")
    assert role.id is not None
    assert role.name == "admin"

    fetched = await service.get_by_id(role.id)
    assert fetched is not None

    roles, total = await service.get_list()
    assert total == 1

    updated = await service.update(
        role_id=role.id,
        name="superadmin",
        description="Super Admin",
    )
    assert updated.name == "superadmin"

    await service.delete(role.id)
    assert await service.get_by_id(role.id) is None


@pytest.mark.asyncio
async def test_permission_service_crud(db_session: AsyncSession):
    service = PermissionService(db_session)
    permission = await service.create(
        name="test_permission",
        description="Test permission",
    )
    assert permission.id is not None
    assert permission.name == "test_permission"

    fetched = await service.get_by_id(permission.id)
    assert fetched is not None

    permissions, total = await service.get_list()
    assert total == 1


@pytest.mark.asyncio
async def test_role_permission_linking(db_session: AsyncSession):
    role_service = RoleService(db_session)
    permission_service = PermissionService(db_session)

    role = await role_service.create(name="tester", description="Tester role")
    permission = await permission_service.create(
        name="test_perm",
        description="Test permission",
    )

    await role_service.update(role_id=role.id, permission_ids=[permission.id])
    updated_role = await role_service.get_by_id(role.id)
    assert updated_role is not None

    links = await db_session.execute(
        select(RolePermission).where(RolePermission.role_id == updated_role.id)
    )
    assert len(list(links.scalars().all())) == 1
