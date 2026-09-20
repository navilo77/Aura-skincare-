
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import Coupon
from app.modules.admin.repositories.base import BaseRepository


class CouponRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Coupon)

    async def get_by_code(self, code: str) -> Coupon | None:
        return await self.get_by_field("code", code)

    async def exists_by_code(self, code: str) -> bool:
        return await self.exists_by_field("code", code)
