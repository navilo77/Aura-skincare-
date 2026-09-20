
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.marketing_ai.models import (
    MarketingAILog,
    MarketingAsset,
    MarketingCampaign,
    MarketingContent,
    MarketingHistory,
    MarketingTemplate,
)
from app.modules.marketing_ai.repositories.base import BaseRepository


class MarketingCampaignRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MarketingCampaign)


class MarketingTemplateRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MarketingTemplate)

    async def get_active(self) -> list[MarketingTemplate]:
        result = await self.session.execute(
            select(MarketingTemplate).where(MarketingTemplate.is_active == True)  # noqa: E712
        )
        return list(result.scalars().all())


class MarketingContentRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MarketingContent)


class MarketingHistoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MarketingHistory)


class MarketingAssetRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MarketingAsset)


class MarketingAILogRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MarketingAILog)
