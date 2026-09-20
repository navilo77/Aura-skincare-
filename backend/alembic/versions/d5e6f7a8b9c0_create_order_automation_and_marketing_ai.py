"""create order automation and marketing ai tables

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2026-09-19 11:00:00.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'd5e6f7a8b9c0'
down_revision: str | None = 'c4d5e6f7a8b9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('inventory_transactions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('warehouse_id', sa.UUID(), nullable=False),
    sa.Column('quantity_change', sa.Integer(), nullable=False),
    sa.Column('transaction_type', sa.Enum('purchase', 'sale', 'return', 'adjustment', 'reservation', 'release', 'transfer_in', 'transfer_out', name='inventory_transaction_type'), nullable=False),
    sa.Column('reference_type', sa.String(length=50), nullable=True),
    sa.Column('reference_id', sa.UUID(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('performed_by', sa.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_transactions_product_id'), 'inventory_transactions', ['product_id'], unique=False)
    op.create_index(op.f('ix_inventory_transactions_warehouse_id'), 'inventory_transactions', ['warehouse_id'], unique=False)

    op.create_table('order_events',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('event_type', sa.Enum('pending', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled', 'refunded', name='order_event_type'), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('extra_metadata', sa.Text(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_events_order_id'), 'order_events', ['order_id'], unique=False)

    op.create_table('automation_jobs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('job_type', sa.Enum('inventory_sync', 'low_stock_scan', 'expired_reservation_cleanup', 'order_event_processing', name='automation_job_type'), nullable=False),
    sa.Column('status', sa.Enum('pending', 'running', 'completed', 'failed', name='automation_job_status'), nullable=False, server_default='pending'),
    sa.Column('scheduled_at', sa.DateTime(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('extra_metadata', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_automation_jobs_job_type'), 'automation_jobs', ['job_type'], unique=False)

    op.create_table('inventory_alerts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('warehouse_id', sa.UUID(), nullable=False),
    sa.Column('alert_type', sa.Enum('low_stock', 'out_of_stock', 'negative_inventory', name='inventory_alert_type'), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('is_resolved', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('resolved_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_alerts_product_id'), 'inventory_alerts', ['product_id'], unique=False)
    op.create_index(op.f('ix_inventory_alerts_warehouse_id'), 'inventory_alerts', ['warehouse_id'], unique=False)
    op.create_index(op.f('ix_inventory_alerts_alert_type'), 'inventory_alerts', ['alert_type'], unique=False)

    op.create_table('marketing_campaigns',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('marketing_templates',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('content_type', sa.String(length=50), nullable=False),
    sa.Column('prompt', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('marketing_contents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('campaign_id', sa.UUID(), nullable=True),
    sa.Column('template_id', sa.UUID(), nullable=True),
    sa.Column('content_type', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('extra_metadata', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('marketing_history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('content_id', sa.UUID(), nullable=True),
    sa.Column('action', sa.String(length=50), nullable=False),
    sa.Column('extra_metadata', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('marketing_assets',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('content_id', sa.UUID(), nullable=True),
    sa.Column('asset_type', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(length=512), nullable=False),
    sa.Column('extra_metadata', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('marketing_ai_logs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('agent', sa.String(length=50), nullable=False),
    sa.Column('prompt_version', sa.String(length=50), nullable=True),
    sa.Column('token_usage', sa.Integer(), nullable=True),
    sa.Column('extra_metadata', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('marketing_ai_logs')
    op.drop_table('marketing_assets')
    op.drop_table('marketing_history')
    op.drop_table('marketing_contents')
    op.drop_table('marketing_templates')
    op.drop_table('marketing_campaigns')
    op.drop_index(op.f('ix_inventory_alerts_alert_type'), table_name='inventory_alerts')
    op.drop_index(op.f('ix_inventory_alerts_warehouse_id'), table_name='inventory_alerts')
    op.drop_index(op.f('ix_inventory_alerts_product_id'), table_name='inventory_alerts')
    op.drop_table('inventory_alerts')
    op.drop_index(op.f('ix_automation_jobs_job_type'), table_name='automation_jobs')
    op.drop_table('automation_jobs')
    op.drop_index(op.f('ix_order_events_order_id'), table_name='order_events')
    op.drop_table('order_events')
    op.drop_index(op.f('ix_inventory_transactions_warehouse_id'), table_name='inventory_transactions')
    op.drop_index(op.f('ix_inventory_transactions_product_id'), table_name='inventory_transactions')
    op.drop_table('inventory_transactions')
    op.execute('DROP TYPE IF EXISTS inventory_transaction_type')
    op.execute('DROP TYPE IF EXISTS order_event_type')
    op.execute('DROP TYPE IF EXISTS automation_job_type')
    op.execute('DROP TYPE IF EXISTS automation_job_status')
    op.execute('DROP TYPE IF EXISTS inventory_alert_type')
