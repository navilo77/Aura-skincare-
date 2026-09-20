import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.wishlist.repositories.wishlist import (
    WishlistItemRepository,
    WishlistRepository,
)
from app.modules.wishlist.services.wishlist import WishlistService


@pytest.mark.asyncio
async def test_wishlist_repository_create_and_get(db_session: AsyncSession):
    repo = WishlistRepository(db_session)
    wishlist = await repo.create(user_id=uuid.uuid4())
    assert wishlist.id is not None

    fetched = await repo.get_by_user_id(wishlist.user_id)
    assert fetched is not None
    assert fetched.id == wishlist.id


@pytest.mark.asyncio
async def test_wishlist_service_add_prevents_duplicates(db_session: AsyncSession):
    service = WishlistService(db_session)
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()

    item1 = await service.add_item(user_id=user_id, product_id=product_id)
    item2 = await service.add_item(user_id=user_id, product_id=product_id)

    assert item1.id == item2.id

    items = await service.get_wishlist_items(user_id)
    assert len(items) == 1


@pytest.mark.asyncio
async def test_wishlist_service_remove(db_session: AsyncSession):
    service = WishlistService(db_session)
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()

    await service.add_item(user_id=user_id, product_id=product_id)
    await service.remove_item(user_id=user_id, product_id=product_id)

    items = await service.get_wishlist_items(user_id)
    assert len(items) == 0


@pytest.mark.asyncio
async def test_wishlist_item_repository_crud(db_session: AsyncSession):
    wishlist_repo = WishlistRepository(db_session)
    wishlist = await wishlist_repo.create(user_id=uuid.uuid4())

    item_repo = WishlistItemRepository(db_session)
    item = await item_repo.create(
        wishlist_id=wishlist.id,
        product_id=uuid.uuid4(),
    )
    assert item.id is not None

    fetched = await item_repo.get_by_id(item.id)
    assert fetched is not None

    await item_repo.delete(item.id)
    assert await item_repo.get_by_id(item.id) is None
