import asyncio
import sys
from pathlib import Path

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.settings import settings
from app.modules.product.models.brand import Brand
from app.modules.product.models.category import Category
from app.modules.product.models.product import Product
from app.shared.database.base import Base


async def seed() -> None:
    engine = create_async_engine(settings.database_url, echo=settings.database_echo)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        result = await session.execute(Category.__table__.select().limit(1))
        if result.first():
            print("Seed data already exists. Skipping.")
            return

        categories = [
            Category(
                name="Cleanser",
                slug="cleanser",
                description="Facial cleansers",
                is_active=True,
            ),
            Category(
                name="Toner",
                slug="toner",
                description="Facial toners",
                is_active=True,
            ),
            Category(
                name="Serum",
                slug="serum",
                description="Treatment serums",
                is_active=True,
            ),
            Category(
                name="Moisturizer",
                slug="moisturizer",
                description="Face moisturizers",
                is_active=True,
            ),
            Category(
                name="Sunscreen",
                slug="sunscreen",
                description="SPF protection",
                is_active=True,
            ),
        ]
        session.add_all(categories)

        brands = [
            Brand(
                name="Aura Botanicals",
                slug="aura-botanicals",
                description="Natural skincare",
                is_active=True,
            ),
            Brand(
                name="PureGlow",
                slug="pureglow",
                description="Clinical skincare",
                is_active=True,
            ),
            Brand(
                name="DermaPure",
                slug="dermapure",
                description="Dermatologist tested",
                is_active=True,
            ),
        ]
        session.add_all(brands)

        await session.flush()

        products = [
            Product(
                name="Gentle Foam Cleanser",
                slug="gentle-foam-cleanser",
                sku="AURA-CLN-001",
                price=29.99,
                currency="USD",
                short_description="A gentle daily cleanser",
                description="A gentle daily cleanser for all skin types.",
                status="active",
                product_type="simple",
                stock_quantity=100,
                brand_id=brands[0].id,
                category_id=categories[0].id,
                is_active=True,
            ),
            Product(
                name="Hydrating Toner",
                slug="hydrating-toner",
                sku="AURA-TON-001",
                price=24.99,
                currency="USD",
                short_description="Hydrating facial toner",
                description="A hydrating toner that preps skin for serums.",
                status="active",
                product_type="simple",
                stock_quantity=75,
                brand_id=brands[0].id,
                category_id=categories[1].id,
                is_active=True,
            ),
            Product(
                name="Vitamin C Serum",
                slug="vitamin-c-serum",
                sku="AURA-SRM-001",
                price=49.99,
                currency="USD",
                short_description="Brightening vitamin C serum",
                description="A powerful vitamin C serum for brightening.",
                status="active",
                product_type="simple",
                stock_quantity=50,
                brand_id=brands[1].id,
                category_id=categories[2].id,
                is_active=True,
            ),
            Product(
                name="Daily Moisturizer SPF 30",
                slug="daily-moisturizer-spf-30",
                sku="AURA-MOI-001",
                price=34.99,
                currency="USD",
                short_description="Lightweight daily moisturizer with SPF",
                description="A lightweight moisturizer with SPF 30 protection.",
                status="active",
                product_type="simple",
                stock_quantity=120,
                brand_id=brands[2].id,
                category_id=categories[3].id,
                is_active=True,
            ),
            Product(
                name="Invisible Shield Sunscreen",
                slug="invisible-shield-sunscreen",
                sku="AURA-SUN-001",
                price=39.99,
                currency="USD",
                short_description="Invisible broad-spectrum SPF 50",
                description="An invisible broad-spectrum SPF 50 sunscreen.",
                status="active",
                product_type="simple",
                stock_quantity=80,
                brand_id=brands[1].id,
                category_id=categories[4].id,
                is_active=True,
            ),
        ]
        session.add_all(products)
        await session.commit()
        print("Seed data inserted successfully.")


if __name__ == "__main__":
    from sqlalchemy.ext.asyncio import async_sessionmaker

    asyncio.run(seed())
