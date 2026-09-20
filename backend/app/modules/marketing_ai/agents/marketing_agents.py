from typing import Any

from app.modules.marketing_ai.schemas.marketing import (
    MarketingContentRead,
)


class BaseMarketingAgent:
    name: str = ""

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        raise NotImplementedError


class ContentAgent(BaseMarketingAgent):
    name = "content"

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        return MarketingContentRead(
            id=payload.get("id", "00000000-0000-0000-0000-000000000000"),
            campaign_id=payload.get("campaign_id"),
            template_id=payload.get("template_id"),
            content_type=payload.get("content_type", "text"),
            title=payload.get("title"),
            body=payload.get("body", ""),
            metadata=payload.get("metadata"),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
        )


class CampaignAgent(BaseMarketingAgent):
    name = "campaign"

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        return MarketingContentRead(
            id=payload.get("id", "00000000-0000-0000-0000-000000000000"),
            campaign_id=payload.get("campaign_id"),
            template_id=payload.get("template_id"),
            content_type="campaign",
            title=payload.get("title"),
            body=payload.get("body", ""),
            metadata=payload.get("metadata"),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
        )


class SEOAgent(BaseMarketingAgent):
    name = "seo"

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        return MarketingContentRead(
            id=payload.get("id", "00000000-0000-0000-0000-000000000000"),
            campaign_id=payload.get("campaign_id"),
            template_id=payload.get("template_id"),
            content_type="seo",
            title=payload.get("title"),
            body=payload.get("body", ""),
            metadata=payload.get("metadata"),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
        )


class EmailAgent(BaseMarketingAgent):
    name = "email"

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        return MarketingContentRead(
            id=payload.get("id", "00000000-0000-0000-0000-000000000000"),
            campaign_id=payload.get("campaign_id"),
            template_id=payload.get("template_id"),
            content_type="email",
            title=payload.get("title"),
            body=payload.get("body", ""),
            metadata=payload.get("metadata"),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
        )


class SocialAgent(BaseMarketingAgent):
    name = "social"

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        return MarketingContentRead(
            id=payload.get("id", "00000000-0000-0000-0000-000000000000"),
            campaign_id=payload.get("campaign_id"),
            template_id=payload.get("template_id"),
            content_type="social",
            title=payload.get("title"),
            body=payload.get("body", ""),
            metadata=payload.get("metadata"),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
        )


class AnalyticsAgent(BaseMarketingAgent):
    name = "analytics"

    async def generate(self, payload: dict[str, Any]) -> MarketingContentRead:
        return MarketingContentRead(
            id=payload.get("id", "00000000-0000-0000-0000-000000000000"),
            campaign_id=payload.get("campaign_id"),
            template_id=payload.get("template_id"),
            content_type="analytics",
            title=payload.get("title"),
            body=payload.get("body", ""),
            metadata=payload.get("metadata"),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
        )
