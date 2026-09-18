import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)


class RoleCreate(RoleBase):
    permission_ids: list[uuid.UUID] = []


class RoleUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    permission_ids: list[uuid.UUID] | None = None


class RoleRead(RoleBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    permissions: list[PermissionRead] = []
