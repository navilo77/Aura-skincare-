"""create analytics module tables

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-09-17 16:18:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "e5f6a7b8c9d0"
down_revision: str | None = "d4e5f6a7b8c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "analytics_events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("event_name", sa.String(length=100), nullable=False),
        sa.Column("event_category", sa.String(length=100), nullable=False),
        sa.Column("properties", sa.Text(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_analytics_events_event_name"),
        "analytics_events",
        ["event_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_analytics_events_event_category"),
        "analytics_events",
        ["event_category"],
        unique=False,
    )
    op.create_index(
        op.f("ix_analytics_events_user_id"),
        "analytics_events",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_analytics_events_session_id"),
        "analytics_events",
        ["session_id"],
        unique=False,
    )
    op.create_table(
        "metrics",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("metric_name", sa.String(length=100), nullable=False),
        sa.Column("metric_value", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "metric_type",
            sa.Enum("counter", "gauge", "histogram", name="metric_type"),
            nullable=False,
        ),
        sa.Column("dimensions", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_metrics_metric_name"), "metrics", ["metric_name"], unique=False
    )
    op.create_index(
        op.f("ix_metrics_recorded_at"), "metrics", ["recorded_at"], unique=False
    )
    op.create_table(
        "dashboards",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("layout", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(None, "analytics_events", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "analytics_events", type_="foreignkey")
    op.drop_index(op.f("ix_analytics_events_session_id"), table_name="analytics_events")
    op.drop_index(op.f("ix_analytics_events_user_id"), table_name="analytics_events")
    op.drop_index(
        op.f("ix_analytics_events_event_category"), table_name="analytics_events"
    )
    op.drop_index(op.f("ix_analytics_events_event_name"), table_name="analytics_events")
    op.drop_table("analytics_events")
    op.drop_index(op.f("ix_metrics_recorded_at"), table_name="metrics")
    op.drop_index(op.f("ix_metrics_metric_name"), table_name="metrics")
    op.drop_table("metrics")
    op.drop_table("dashboards")
