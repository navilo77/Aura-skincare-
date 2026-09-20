from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class MarketingCampaign(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "marketing_campaigns"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    start_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    end_date: Mapped[str | None] = mapped_column(String(50), nullable=True)


class MarketingTemplate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "marketing_templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(String(10), nullable=False, default="true")


class MarketingContent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "marketing_contents"

    campaign_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("marketing_campaigns.id"), nullable=True)
    template_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("marketing_templates.id"), nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    extra_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)


class MarketingHistory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "marketing_history"

    content_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    extra_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)


class MarketingAsset(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "marketing_assets"

    content_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    extra_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)


class MarketingAILog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "marketing_ai_logs"

    agent: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    token_usage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    extra_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)
