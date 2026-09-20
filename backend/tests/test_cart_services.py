import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cart.repositories.cart import CartItemRepository, CartRepository
from app.modules.cart.services.cart import CartService


@pytest.mark.asyncio
async def test_cart_repository_create_and_get(db_session: AsyncSession):
    repo = CartRepository(db_session)
    cart = await repo.create(user_id=uuid.uuid4())
    assert cart.id is not None

    fetched = await repo.get_by_user_id(cart.user_id)
    assert fetched is not None
    assert fetched.id == cart.id


@pytest.mark.asyncio
async def test_cart_service_add_and_summary(db_session: AsyncSession):
    service = CartService(db_session)
    user_id = uuid.uuid4()

    item = await service.add_item(
        user_id=user_id,
        product_id=uuid.uuid4(),
        quantity=2,
        unit_price=10.0,
    )
    assert item.id is not None
    assert item.quantity == 2

    total_items, total_amount = await service.get_cart_summary(user_id)
    assert total_items == 2
    assert total_amount == 20.0


@pytest.mark.asyncio
async def test_cart_service_update_and_remove(db_session: AsyncSession):
    service = CartService(db_session)
    user_id = uuid.uuid4()

    item = await service.add_item(
        user_id=user_id,
        product_id=uuid.uuid4(),
        quantity=1,
        unit_price=5.0,
    )

    updated = await service.update_item(item.id, quantity=3, unit_price=5.0)
    assert updated.quantity == 3
    assert updated.subtotal == 15.0

    await service.remove_item(updated.id)
    items = await service.get_cart_items(user_id)
    assert len(items) == 0


@pytest.mark.asyncio
async def test_cart_item_repository_create_update_delete(db_session: AsyncSession):
    cart_repo = CartRepository(db_session)
    cart = await cart_repo.create(user_id=uuid.uuid4())

    item_repo = CartItemRepository(db_session)
    item = await item_repo.create(
        cart_id=cart.id,
        product_id=uuid.uuid4(),
        quantity=1,
        unit_price=10.0,
        subtotal=10.0,
    )
    assert item.id is not None

    item.quantity = 2
    updated = await item_repo.update(item, quantity=2, subtotal=20.0)
    assert updated.quantity == 2

    await item_repo.delete(item.id)
    assert await item_repo.get_by_id(item.id) is None
