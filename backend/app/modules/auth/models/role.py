from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.auth.models import Permission as PermissionType, Role as RoleType

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Permission(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    roles: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )


class Role(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class RolePermission(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("roles.id"), nullable=False, index=True
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("permissions.id"), nullable=False, index=True
    )

    role: Mapped["Role"] = relationship("Role", back_populates="permissions")
    permission: Mapped["Permission"] = relationship(
        "Permission", back_populates="roles"
    )
