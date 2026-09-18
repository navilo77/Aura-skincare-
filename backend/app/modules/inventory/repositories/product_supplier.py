import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import ProductSupplier
from app.modules.inventory.repositories.base import BaseRepository


class ProductSupplierRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductSupplier)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductSupplier]:
        result = await self.session.execute(
            select(ProductSupplier).where(ProductSupplier.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_supplier(self, supplier_id: uuid.UUID) -> list[ProductSupplier]:
        result = await self.session.execute(
            select(ProductSupplier).where(ProductSupplier.supplier_id == supplier_id)
        )
        return list(result.scalars().all())

    async def get_preferred(self, product_id: uuid.UUID) -> ProductSupplier | None:
        result = await self.session.execute(
            select(ProductSupplier).where(
                ProductSupplier.product_id == product_id,
                ProductSupplier.is_preferred == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def exists_by_product_and_supplier(
        self, product_id: uuid.UUID, supplier_id: uuid.UUID
    ) -> bool:
        result = await self.session.execute(
            select(ProductSupplier).where(
                ProductSupplier.product_id == product_id,
                ProductSupplier.supplier_id == supplier_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_by_product_and_supplier(
        self, product_id: uuid.UUID, supplier_id: uuid.UUID
    ) -> ProductSupplier | None:
        result = await self.session.execute(
            select(ProductSupplier).where(
                ProductSupplier.product_id == product_id,
                ProductSupplier.supplier_id == supplier_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, product_supplier: ProductSupplier) -> ProductSupplier:
        self.session.add(product_supplier)
        await self.session.flush()
        return product_supplier

    async def update(self, product_supplier: ProductSupplier) -> ProductSupplier:
        await self.session.merge(product_supplier)
        await self.session.flush()
        return product_supplier
