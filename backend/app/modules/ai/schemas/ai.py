from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ConversationRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    session_id: str
    agent_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationCreate(BaseModel):
    user_id: uuid.UUID | None = None
    session_id: str
    agent_type: str = "router"


class MessageRead(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    tool_calls: str | None
    extra_metadata: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    conversation_id: uuid.UUID
    role: str = "user"
    content: str
    tool_calls: str | None = None
    extra_metadata: str | None = None


class ChatRequest(BaseModel):
    message: str
    session_id: str
    user_id: uuid.UUID | None = None


class ChatResponse(BaseModel):
    message: str
    session_id: str
    agent_type: str
    tool_calls: list[dict[str, Any]] | None = None


class SessionStateRead(BaseModel):
    id: uuid.UUID
    session_id: str
    user_id: uuid.UUID | None
    current_agent: str
    intent: str | None
    context: str | None
    is_active: bool
    last_activity_at: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
