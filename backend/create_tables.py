import asyncio
import importlib
import pkgutil
import sys
import traceback

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.shared.database.base import Base

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def import_all_model_modules() -> None:
    base_package = "app.modules"
    for module_info in pkgutil.walk_packages([base_package.replace(".", "/")], prefix=f"{base_package}."):
        if ".models." in module_info.name or module_info.name.endswith(".models"):
            try:
                importlib.import_module(module_info.name)
            except Exception:
                print(f"Failed to import {module_info.name}:")
                traceback.print_exc()


async def main() -> None:
    import_all_model_modules()
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Tables created successfully")


if __name__ == "__main__":
    asyncio.run(main())
