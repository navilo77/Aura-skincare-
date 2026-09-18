import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import ProductSupplier
from app.modules.inventory.repositories.product_supplier import (
    ProductSupplierRepository,
)
from app.modules.inventory.repositories.supplier import SupplierRepository


class ProductSupplierService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductSupplierRepository(session)
        self.supplier_repository = SupplierRepository(session)

    async def create(
        self,
        product_id: uuid.UUID,
        supplier_id: uuid.UUID,
        cost_price: float,
        is_preferred: bool = False,
    ) -> ProductSupplier:
        if await self.repository.exists_by_product_and_supplier(
            product_id, supplier_id
        ):
            raise ValueError("Product supplier link already exists")

        supplier = await self.supplier_repository.get_by_id(supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")

        product_supplier = ProductSupplier(
            product_id=product_id,
            supplier_id=supplier_id,
            cost_price=cost_price,
            is_preferred=is_preferred,
        )
        return await self.repository.create(product_supplier)

    async def delete(self, product_id: uuid.UUID, supplier_id: uuid.UUID) -> None:
        link = await self.repository.get_by_product_and_supplier(
            product_id, supplier_id
        )
        if not link:
            raise ValueError("Product supplier link not found")
        await self.repository.delete(link.id)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductSupplier]:
        return await self.repository.get_by_product(product_id)

    async def get_by_supplier(self, supplier_id: uuid.UUID) -> list[ProductSupplier]:
        return await self.repository.get_by_supplier(supplier_id)
