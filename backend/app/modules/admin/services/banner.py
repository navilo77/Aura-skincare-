import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import Banner
from app.modules.admin.repositories.banner import BannerRepository


class BannerService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = BannerRepository(session)

    async def create(self, **kwargs: Any) -> Banner:
        banner = Banner(**kwargs)
        return await self.repository.create(banner)

    async def get_by_id(self, banner_id: uuid.UUID) -> Banner | None:
        return await self.repository.get_by_id(banner_id)

    async def get_list(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[Banner], int]:
        return await self.repository.get_list(skip=skip, limit=limit)

    async def update(self, banner_id: uuid.UUID, **kwargs: Any) -> Banner:
        banner = await self.repository.get_by_id(banner_id)
        if not banner:
            raise ValueError("Banner not found")
        updated = await self.repository.update(banner, **kwargs)
        return updated

    async def delete(self, banner_id: uuid.UUID) -> None:
        banner = await self.repository.get_by_id(banner_id)
        if not banner:
            raise ValueError("Banner not found")
        await self.repository.delete(banner_id)
