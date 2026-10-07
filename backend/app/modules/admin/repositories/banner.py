from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import Banner
from app.modules.admin.repositories.base import BaseRepository


class BannerRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Banner)

    async def list_by_position(self, position: str) -> list[Banner]:
        return await self.get_list_by_field("position", position)
