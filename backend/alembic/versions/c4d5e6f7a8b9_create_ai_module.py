"""create ai module tables

Revision ID: c4d5e6f7a8b9
Revises: b2c3d4e5f6a8
Create Date: 2026-09-19 10:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c4d5e6f7a8b9"
down_revision: str | None = "b2c3d4e5f6a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ai_conversations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column(
            "agent_type",
            sa.Enum("router", "customer", "admin", "marketing", name="ai_agent_type"),
            nullable=False,
            server_default="router",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ai_conversations_session_id"),
        "ai_conversations",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ai_conversations_user_id"),
        "ai_conversations",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ai_conversations_agent_type"),
        "ai_conversations",
        ["agent_type"],
        unique=False,
    )

    op.create_table(
        "ai_messages",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("conversation_id", sa.UUID(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("user", "assistant", "system", name="ai_message_role"),
            nullable=False,
            server_default="user",
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tool_calls", sa.Text(), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ai_messages_conversation_id"),
        "ai_messages",
        ["conversation_id"],
        unique=False,
    )
    op.create_index(op.f("ix_ai_messages_role"), "ai_messages", ["role"], unique=False)

    op.create_table(
        "ai_session_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column(
            "current_agent",
            sa.Enum("router", "customer", "admin", "marketing", name="ai_agent_type"),
            nullable=False,
            server_default="router",
        ),
        sa.Column("intent", sa.String(length=100), nullable=True),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_activity_at", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ai_session_states_session_id"),
        "ai_session_states",
        ["session_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_ai_session_states_user_id"),
        "ai_session_states",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "ai_tool_call_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column("message_id", sa.UUID(), nullable=True),
        sa.Column("tool_name", sa.String(length=100), nullable=False),
        sa.Column("arguments", sa.Text(), nullable=True),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("success", "error", "timeout", name="ai_tool_status"),
            nullable=False,
            server_default="success",
        ),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ai_tool_call_logs_session_id"),
        "ai_tool_call_logs",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ai_tool_call_logs_tool_name"),
        "ai_tool_call_logs",
        ["tool_name"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_ai_tool_call_logs_tool_name"), table_name="ai_tool_call_logs"
    )
    op.drop_index(
        op.f("ix_ai_tool_call_logs_session_id"), table_name="ai_tool_call_logs"
    )
    op.drop_table("ai_tool_call_logs")
    op.drop_index(op.f("ix_ai_session_states_user_id"), table_name="ai_session_states")
    op.drop_index(
        op.f("ix_ai_session_states_session_id"), table_name="ai_session_states"
    )
    op.drop_table("ai_session_states")
    op.drop_index(op.f("ix_ai_messages_role"), table_name="ai_messages")
    op.drop_index(op.f("ix_ai_messages_conversation_id"), table_name="ai_messages")
    op.drop_table("ai_messages")
    op.drop_index(op.f("ix_ai_conversations_agent_type"), table_name="ai_conversations")
    op.drop_index(op.f("ix_ai_conversations_user_id"), table_name="ai_conversations")
    op.drop_index(op.f("ix_ai_conversations_session_id"), table_name="ai_conversations")
    op.drop_table("ai_conversations")
    op.execute("DROP TYPE IF EXISTS ai_agent_type")
    op.execute("DROP TYPE IF EXISTS ai_message_role")
    op.execute("DROP TYPE IF EXISTS ai_tool_status")
