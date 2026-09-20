import pytest


@pytest.mark.asyncio
async def test_profile_requires_auth(client):
    response = await client.get("/api/v1/profile")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_profile_addresses_require_auth(client):
    response = await client.get("/api/v1/profile/addresses")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_profile_orders_require_auth(client):
    response = await client.get("/api/v1/profile/orders")
    assert response.status_code == 401
