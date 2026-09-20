from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.marketing_ai.models import (
    MarketingAILog,
    MarketingAsset,
    MarketingCampaign,
    MarketingContent,
    MarketingHistory,
    MarketingTemplate,
)
from app.modules.marketing_ai.repositories.marketing import (
    MarketingAILogRepository,
    MarketingAssetRepository,
    MarketingCampaignRepository,
    MarketingContentRepository,
    MarketingHistoryRepository,
    MarketingTemplateRepository,
)


class MarketingCampaignService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MarketingCampaignRepository(session)

    async def create(self, **kwargs: Any) -> MarketingCampaign:
        campaign = MarketingCampaign(**kwargs)
        return await self.repository.create(campaign)

    async def get_list(self, skip: int = 0, limit: int = 20) -> tuple[list[MarketingCampaign], int]:
        return await self.repository.get_list(skip=skip, limit=limit)


class MarketingTemplateService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MarketingTemplateRepository(session)

    async def create(self, **kwargs: Any) -> MarketingTemplate:
        template = MarketingTemplate(**kwargs)
        return await self.repository.create(template)

    async def get_active(self) -> list[MarketingTemplate]:
        return await self.repository.get_active()


class MarketingContentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MarketingContentRepository(session)
        self.history_repository = MarketingHistoryRepository(session)
        self.asset_repository = MarketingAssetRepository(session)

    async def create(self, **kwargs: Any) -> MarketingContent:
        content = MarketingContent(**kwargs)
        return await self.repository.create(content)

    async def get_list(self, skip: int = 0, limit: int = 20) -> tuple[list[MarketingContent], int]:
        return await self.repository.get_list(skip=skip, limit=limit)


class MarketingHistoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MarketingHistoryRepository(session)

    async def create(self, **kwargs: Any) -> MarketingHistory:
        history = MarketingHistory(**kwargs)
        return await self.repository.create(history)


class MarketingAssetService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MarketingAssetRepository(session)

    async def create(self, **kwargs: Any) -> MarketingAsset:
        asset = MarketingAsset(**kwargs)
        return await self.repository.create(asset)


class MarketingAILogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MarketingAILogRepository(session)

    async def create(self, **kwargs: Any) -> MarketingAILog:
        log = MarketingAILog(**kwargs)
        return await self.repository.create(log)
