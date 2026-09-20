
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import AdminSettings
from app.modules.admin.repositories.base import BaseRepository


class AdminSettingsRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AdminSettings)

    async def get_by_key(self, key: str) -> AdminSettings | None:
        return await self.get_by_field("key", key)

    async def exists_by_key(self, key: str) -> bool:
        return await self.exists_by_field("key", key)
