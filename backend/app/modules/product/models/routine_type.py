from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class RoutineType(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "routine_types"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )

    product_routines: Mapped[list["ProductRoutine"]] = relationship(
        "ProductRoutine",
        back_populates="routine_type",
        cascade="all, delete-orphan",
    )
