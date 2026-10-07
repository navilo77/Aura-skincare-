import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductBenefit
from app.modules.product.repositories.product_benefit import (
    ProductBenefitRepository,
)


class ProductBenefitService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductBenefitRepository(session)

    async def link(
        self, product_id: uuid.UUID, benefit_id: uuid.UUID
    ) -> ProductBenefit:
        link = ProductBenefit(product_id=product_id, benefit_id=benefit_id)
        return await self.repository.create(link)

    async def unlink(self, product_id: uuid.UUID, benefit_id: uuid.UUID) -> None:
        links = await self.repository.get_by_product(product_id)
        for link in links:
            if link.benefit_id == benefit_id:
                await self.repository.delete(link.id)

    async def get_product_benefits(self, product_id: uuid.UUID) -> list[ProductBenefit]:
        return await self.repository.get_by_product(product_id)
