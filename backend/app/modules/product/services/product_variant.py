from typing import Any

import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductVariant
from app.modules.product.repositories.product import ProductRepository
from app.modules.product.repositories.product_variant import ProductVariantRepository


class ProductVariantService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductVariantRepository(session)
        self.product_repository = ProductRepository(session)

    async def create(
        self,
        product_id: uuid.UUID,
        name: str,
        sku: str,
        price: Decimal,
        stock_quantity: int = 0,
        attributes: dict[str, Any] | None = None,
        is_active: bool = True,
    ) -> ProductVariant:
        sku = sku.upper()

        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        if await self.repository.exists_by_sku(sku):
            raise ValueError("Product variant SKU already exists")

        variant = ProductVariant(
            product_id=product_id,
            name=name,
            sku=sku,
            price=price,
            stock_quantity=stock_quantity,
            attributes=attributes,
            is_active=is_active,
        )
        return await self.repository.create(variant)

    async def update(
        self,
        variant_id: uuid.UUID,
        name: str | None = None,
        sku: str | None = None,
        price: Decimal | None = None,
        stock_quantity: int | None = None,
        attributes: dict[str, Any] | None = None,
        is_active: bool | None = None,
    ) -> ProductVariant:
        variant = await self.repository.get_by_id(variant_id)
        if not variant:
            raise ValueError("Product variant not found")

        if sku is not None:
            sku = sku.upper()
            if await self.repository.exists_by_sku_excluding_id(sku, variant_id):
                raise ValueError("Product variant SKU already exists")
            variant.sku = sku

        if name is not None:
            variant.name = name
        if price is not None:
            variant.price = price
        if stock_quantity is not None:
            variant.stock_quantity = stock_quantity
        if attributes is not None:
            variant.attributes = attributes
        if is_active is not None:
            variant.is_active = is_active

        return await self.repository.update(variant)

    async def delete(self, variant_id: uuid.UUID) -> None:
        variant = await self.repository.get_by_id(variant_id)
        if not variant:
            raise ValueError("Product variant not found")
        await self.repository.delete(variant_id)

    async def get_by_id(self, variant_id: uuid.UUID) -> ProductVariant | None:
        return await self.repository.get_by_id(variant_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        product_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[ProductVariant], int]:
        return await self.repository.get_list(
            skip=skip,
            limit=limit,
            product_id=product_id,
            is_active=is_active,
            search=search,
        )

    async def get_by_product(
        self,
        product_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[ProductVariant]:
        return await self.repository.get_by_product(product_id, skip=skip, limit=limit)
