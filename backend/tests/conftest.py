import asyncio
import os
import sys

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.modules.admin.models import (
    activity_log as activity_log_model,  # noqa: F401
)
from app.modules.admin.models import (
    admin_settings as admin_settings_model,  # noqa: F401
)
from app.modules.admin.models import (
    audit_log as audit_log_model,  # noqa: F401
)
from app.modules.admin.models import (
    banner as banner_model,  # noqa: F401
)
from app.modules.admin.models import coupon as coupon_model  # noqa: F401
from app.modules.auth.models import (
    email_verification as email_verification_model,  # noqa: F401
)
from app.modules.auth.models import user as user_model  # noqa: F401
from app.modules.cart.models import cart as cart_model  # noqa: F401
from app.modules.customer.models import (
    address as address_model,  # noqa: F401
)
from app.modules.customer.models import (
    conversation as conversation_model,  # noqa: F401
)
from app.modules.customer.models import (
    customer as customer_model,  # noqa: F401
)
from app.modules.knowledge.models import (
    knowledge_chunk as knowledge_chunk_model,  # noqa: F401
)
from app.modules.knowledge.models.knowledge_chunk import KnowledgeChunk  # noqa: F401
from app.modules.order.models import (
    billing_address as billing_address_model,  # noqa: F401
)
from app.modules.order.models import (
    order as order_model,  # noqa: F401
)
from app.modules.order.models import (
    order_item as order_item_model,  # noqa: F401
)
from app.modules.order.models import (
    shipping_address as shipping_address_model,  # noqa: F401
)
from app.modules.payment.models import payment as payment_model  # noqa: F401
from app.modules.product.models import (
    product_variant,  # noqa: F401
)
from app.modules.wishlist.models import wishlist as wishlist_model  # noqa: F401
from app.shared.database.base import Base
from app.shared.database.session import get_db as original_get_db

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=StaticPool)
test_session_factory = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest_asyncio.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = test_session_factory()
    try:
        yield session
    finally:
        await session.close()
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[original_get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
