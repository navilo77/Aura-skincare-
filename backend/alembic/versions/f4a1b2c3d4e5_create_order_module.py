"""create order module

Revision ID: f4a1b2c3d4e5
Revises: 41e2eb274d18
Create Date: 2026-09-17 10:34:29.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'f4a1b2c3d4e5'
down_revision: str | None = '41e2eb274d18'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('shipping_addresses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('address_line1', sa.String(length=255), nullable=False),
    sa.Column('address_line2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_shipping_addresses_order_id'), 'shipping_addresses', ['order_id'], unique=False)
    op.create_table('billing_addresses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('address_line1', sa.String(length=255), nullable=False),
    sa.Column('address_line2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_billing_addresses_order_id'), 'billing_addresses', ['order_id'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled', name='order_status'), nullable=False),
    sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('shipping_address_id', sa.UUID(), nullable=True),
    sa.Column('billing_address_id', sa.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_customer_id'), 'orders', ['customer_id'], unique=False)
    op.create_index(op.f('ix_orders_billing_address_id'), 'orders', ['billing_address_id'], unique=False)
    op.create_index(op.f('ix_orders_shipping_address_id'), 'orders', ['shipping_address_id'], unique=False)
    op.create_index(op.f('ix_orders_status'), 'orders', ['status'], unique=False)
    op.create_table('order_items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_sku', sa.String(length=100), nullable=False),
    sa.Column('variant_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_order_id'), 'order_items', ['order_id'], unique=False)
    op.create_index(op.f('ix_order_items_product_id'), 'order_items', ['product_id'], unique=False)
    op.create_foreign_key(None, 'shipping_addresses', 'orders', ['order_id'], ['id'])
    op.create_foreign_key(None, 'billing_addresses', 'orders', ['order_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'shipping_addresses', ['shipping_address_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'billing_addresses', ['billing_address_id'], ['id'])
    op.create_foreign_key(None, 'order_items', 'orders', ['order_id'], ['id'])
    op.create_foreign_key(None, 'order_items', 'products', ['product_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'billing_addresses', type_='foreignkey')
    op.drop_constraint(None, 'shipping_addresses', type_='foreignkey')
    op.drop_index(op.f('ix_order_items_product_id'), table_name='order_items')
    op.drop_index(op.f('ix_order_items_order_id'), table_name='order_items')
    op.drop_table('order_items')
    op.drop_index(op.f('ix_orders_status'), table_name='orders')
    op.drop_index(op.f('ix_orders_billing_address_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_shipping_address_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_customer_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_billing_addresses_order_id'), table_name='billing_addresses')
    op.drop_table('billing_addresses')
    op.drop_index(op.f('ix_shipping_addresses_order_id'), table_name='shipping_addresses')
    op.drop_table('shipping_addresses')
