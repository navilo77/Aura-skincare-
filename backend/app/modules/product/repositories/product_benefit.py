import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import ProductBenefit
from app.modules.product.repositories.base import BaseRepository


class ProductBenefitRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductBenefit)

    async def get_by_product(self, product_id: uuid.UUID) -> list[ProductBenefit]:
        result = await self.session.execute(
            select(ProductBenefit).where(ProductBenefit.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_benefit(self, benefit_id: uuid.UUID) -> list[ProductBenefit]:
        result = await self.session.execute(
            select(ProductBenefit).where(ProductBenefit.benefit_id == benefit_id)
        )
        return list(result.scalars().all())
