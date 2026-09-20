import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [r[0] for r in result.fetchall()]
        print("Tables:", tables)
    await engine.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
