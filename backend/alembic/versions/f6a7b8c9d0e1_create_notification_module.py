"""create notification module tables

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-09-17 16:25:00.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'f6a7b8c9d0e1'
down_revision: str | None = 'e5f6a7b8c9d0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('notification_templates',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('channel', sa.Enum('email', 'sms', 'push', 'whatsapp', 'messenger', name='notification_channel'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_templates_name'), 'notification_templates', ['name'], unique=True)
    op.create_table('notification_preferences',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('channel', sa.Enum('email', 'sms', 'push', 'whatsapp', 'messenger', name='notification_channel'), nullable=False),
    sa.Column('is_enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_preferences_user_id'), 'notification_preferences', ['user_id'], unique=False)
    op.create_table('notifications',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('template_id', sa.UUID(), nullable=True),
    sa.Column('channel', sa.Enum('email', 'sms', 'push', 'whatsapp', 'messenger', name='notification_channel'), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'sent', 'delivered', 'failed', 'cancelled', name='notification_status'), nullable=False),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('sent_at', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
    op.create_index(op.f('ix_notifications_template_id'), 'notifications', ['template_id'], unique=False)
    op.create_foreign_key(None, 'notification_preferences', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'notifications', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'notifications', 'notification_templates', ['template_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'notifications', type_='foreignkey')
    op.drop_constraint(None, 'notifications', type_='foreignkey')
    op.drop_constraint(None, 'notification_preferences', type_='foreignkey')
    op.drop_index(op.f('ix_notifications_template_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_notification_preferences_user_id'), table_name='notification_preferences')
    op.drop_table('notification_preferences')
    op.drop_index(op.f('ix_notification_templates_name'), table_name='notification_templates')
    op.drop_table('notification_templates')
