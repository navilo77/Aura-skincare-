import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cart.services.cart import CartService


@pytest.mark.asyncio
async def test_cart_requires_auth(client):
    response = await client.get("/api/v1/cart")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_cart_add_item(db_session: AsyncSession):
    from app.modules.auth.services.auth import AuthService
    from app.modules.product.models import Product

    user_service = AuthService(db_session)
    user = await user_service.register(
        email="cart@example.com",
        password="secure123",
        full_name="Cart User",
    )

    product = Product(
        brand_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        name="Test Product",
        slug="test-product",
        sku="TEST-001",
        price=10.0,
        currency="USD",
    )
    db_session.add(product)
    await db_session.flush()

    cart_service = CartService(db_session)
    item = await cart_service.add_item(
        user_id=user.id,
        product_id=product.id,
        quantity=2,
        unit_price=product.price,
    )
    assert item.id is not None


@pytest.mark.asyncio
async def test_wishlist_requires_auth(client):
    response = await client.get("/api/v1/wishlist")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_wishlist_add_duplicate_prevented(db_session: AsyncSession):
    from app.modules.auth.services.auth import AuthService
    from app.modules.product.models import Product
    from app.modules.wishlist.services.wishlist import WishlistService

    user_service = AuthService(db_session)
    user = await user_service.register(
        email="wishlist@example.com",
        password="secure123",
        full_name="Wishlist User",
    )

    product = Product(
        brand_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        name="Wishlist Product",
        slug="wishlist-product",
        sku="WISH-001",
        price=20.0,
        currency="USD",
    )
    db_session.add(product)
    await db_session.flush()

    service = WishlistService(db_session)
    item1 = await service.add_item(user_id=user.id, product_id=product.id)
    item2 = await service.add_item(user_id=user.id, product_id=product.id)
    assert item1.id == item2.id
