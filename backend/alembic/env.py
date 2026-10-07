import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("cwd =", Path.cwd())
print("ROOT =", ROOT)
print("sys.path =", sys.path)

import app  # noqa: F401
import app.modules.admin.models  # noqa: F401
import app.modules.ai.models  # noqa: F401
import app.modules.analytics.models  # noqa: F401
import app.modules.auth.models  # noqa: F401
import app.modules.cart.models  # noqa: F401
import app.modules.customer.models  # noqa: F401
import app.modules.inventory.models  # noqa: F401
import app.modules.marketing_ai.models  # noqa: F401
import app.modules.notification.models  # noqa: F401
import app.modules.order.models  # noqa: F401
import app.modules.order_automation.models  # noqa: F401
import app.modules.payment.models  # noqa: F401
import app.modules.product.models  # noqa: F401
import app.modules.wishlist.models  # noqa: F401
from alembic import context
from app.shared.database.base import Base

env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

config = context.config

if config.config_file_name:
    try:
        fileConfig(config.config_file_name)
    except (FileNotFoundError, KeyError):
        pass

database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
