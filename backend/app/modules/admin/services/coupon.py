import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import Coupon
from app.modules.admin.repositories.coupon import CouponRepository


class CouponService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = CouponRepository(session)

    async def create(self, **kwargs: Any) -> Coupon:
        if await self.repository.exists_by_code(kwargs["code"]):
            raise ValueError("Coupon code already exists")
        coupon = Coupon(**kwargs)
        return await self.repository.create(coupon)

    async def get_by_id(self, coupon_id: uuid.UUID) -> Coupon | None:
        return await self.repository.get_by_id(coupon_id)

    async def get_by_code(self, code: str) -> Coupon | None:
        return await self.repository.get_by_code(code)

    async def get_list(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[Coupon], int]:
        return await self.repository.get_list(skip=skip, limit=limit)

    async def update(self, coupon_id: uuid.UUID, **kwargs: Any) -> Coupon:
        coupon = await self.repository.get_by_id(coupon_id)
        if not coupon:
            raise ValueError("Coupon not found")
        if "code" in kwargs and kwargs["code"] != coupon.code:
            if await self.repository.exists_by_code(kwargs["code"]):
                raise ValueError("Coupon code already exists")
        updated = await self.repository.update(coupon, **kwargs)
        return updated

    async def delete(self, coupon_id: uuid.UUID) -> None:
        coupon = await self.repository.get_by_id(coupon_id)
        if not coupon:
            raise ValueError("Coupon not found")
        await self.repository.delete(coupon_id)
