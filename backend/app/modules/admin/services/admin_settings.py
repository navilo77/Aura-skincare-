from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import AdminSettings
from app.modules.admin.repositories.admin_settings import AdminSettingsRepository


class AdminSettingsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AdminSettingsRepository(session)

    async def get_by_key(self, key: str) -> AdminSettings | None:
        return await self.repository.get_by_key(key)

    async def get_list(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[AdminSettings], int]:
        return await self.repository.get_list(skip=skip, limit=limit)

    async def create(self, **kwargs: Any) -> AdminSettings:
        if await self.repository.exists_by_key(kwargs["key"]):
            raise ValueError("Setting key already exists")
        setting = AdminSettings(**kwargs)
        return await self.repository.create(setting)

    async def update(self, key: str, value: str) -> AdminSettings:
        setting = await self.repository.get_by_key(key)
        if not setting:
            raise ValueError("Setting not found")
        updated = await self.repository.update(setting, value=value)
        return updated

    async def delete(self, key: str) -> None:
        setting = await self.repository.get_by_key(key)
        if not setting:
            raise ValueError("Setting not found")
        await self.repository.delete(setting.id)
