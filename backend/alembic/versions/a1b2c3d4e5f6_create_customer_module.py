"""create customer module

Revision ID: a1b2c3d4e5f6
Revises: feb39ceece7d
Create Date: 2026-09-17 10:34:29.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'a1b2c3d4e5f6'
down_revision: str | None = 'feb39ceece7d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('customers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', 'suspended', name='customer_status'), nullable=False),
    sa.Column('skin_type', sa.String(length=50), nullable=True),
    sa.Column('skin_concerns', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=True)
    op.create_index(op.f('ix_customers_phone'), 'customers', ['phone'], unique=False)
    op.create_index(op.f('ix_customers_status'), 'customers', ['status'], unique=False)
    op.create_table('customer_addresses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('address_line1', sa.String(length=255), nullable=False),
    sa.Column('address_line2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=False),
    sa.Column('is_default', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_addresses_customer_id'), 'customer_addresses', ['customer_id'], unique=False)
    op.create_table('conversations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('channel', sa.Enum('whatsapp', 'messenger', 'instagram', 'website', name='conversation_channel'), nullable=False),
    sa.Column('status', sa.Enum('active', 'closed', 'pending', name='conversation_status'), nullable=False),
    sa.Column('last_message_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_customer_id'), 'conversations', ['customer_id'], unique=False)
    op.create_foreign_key(None, 'customer_addresses', 'customers', ['customer_id'], ['id'])
    op.create_foreign_key(None, 'conversations', 'customers', ['customer_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'conversations', type_='foreignkey')
    op.drop_constraint(None, 'customer_addresses', type_='foreignkey')
    op.drop_index(op.f('ix_conversations_customer_id'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_customer_addresses_customer_id'), table_name='customer_addresses')
    op.drop_table('customer_addresses')
    op.drop_index(op.f('ix_customers_status'), table_name='customers')
    op.drop_index(op.f('ix_customers_phone'), table_name='customers')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
