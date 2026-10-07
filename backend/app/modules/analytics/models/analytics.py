from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import UUID, Boolean, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class AnalyticsEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "analytics_events"

    event_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    properties: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    session_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )


class Metric(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "metrics"

    metric_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    metric_value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    metric_type: Mapped[str] = mapped_column(
        Enum("counter", "gauge", "histogram", name="metric_type"),
        nullable=False,
    )
    dimensions: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[str] = mapped_column(String(50), nullable=False, index=True)


class Dashboard(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "dashboards"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    layout: Mapped[str | None] = mapped_column(Text, nullable=True)
