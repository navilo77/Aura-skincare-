from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.services.admin_settings import AdminSettingsService
from app.modules.admin.services.coupon import CouponService


@pytest.mark.asyncio
async def test_admin_dashboard_requires_admin(client):
    response = await client.get("/api/v1/admin/dashboard")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_admin_coupon_crud(db_session: AsyncSession):
    service = CouponService(db_session)
    coupon = await service.create(
        code="EPIC05TEST",
        discount_type="percentage",
        discount_value=10,
        starts_at=datetime(2099, 1, 1, tzinfo=UTC),
        expires_at=datetime(2099, 12, 31, 23, 59, 59, tzinfo=UTC),
    )
    assert coupon.id is not None

    fetched = await service.get_by_id(coupon.id)
    assert fetched is not None
    assert fetched.code == "EPIC05TEST"


@pytest.mark.asyncio
async def test_admin_settings_create_and_update(db_session: AsyncSession):
    service = AdminSettingsService(db_session)
    setting = await service.create(
        key="site_name",
        value="Aura Skincare",
        description="Site name",
    )
    assert setting.id is not None

    updated = await service.update("site_name", "Aura Skincare Pro")
    assert updated.value == "Aura Skincare Pro"


@pytest.mark.asyncio
async def test_admin_endpoints_reject_customer(client):
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "customer@example.com",
            "password": "secure123",
            "full_name": "Customer User",
        },
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "customer@example.com",
            "password": "secure123",
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 403
