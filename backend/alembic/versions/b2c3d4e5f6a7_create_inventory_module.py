"""create inventory module

Revision ID: b2c3d4e5f6a7
Revises: 41e2eb274d18
Create Date: 2026-09-17 15:38:15.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'b2c3d4e5f6a7'
down_revision: str | None = '41e2eb274d18'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('warehouses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_warehouses_code'), 'warehouses', ['code'], unique=True)
    op.create_table('suppliers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('contact_email', sa.String(length=255), nullable=True),
    sa.Column('contact_phone', sa.String(length=50), nullable=True),
    sa.Column('lead_time_days', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('warehouse_id', sa.UUID(), nullable=False),
    sa.Column('quantity_on_hand', sa.Integer(), nullable=False),
    sa.Column('quantity_reserved', sa.Integer(), nullable=False),
    sa.Column('low_stock_threshold', sa.Integer(), nullable=False),
    sa.Column('is_tracking_enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventories_product_id'), 'inventories', ['product_id'], unique=True)
    op.create_index(op.f('ix_inventories_warehouse_id'), 'inventories', ['warehouse_id'], unique=False)
    op.create_table('product_suppliers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('supplier_id', sa.UUID(), nullable=False),
    sa.Column('cost_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('is_preferred', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_suppliers_product_id'), 'product_suppliers', ['product_id'], unique=False)
    op.create_index(op.f('ix_product_suppliers_supplier_id'), 'product_suppliers', ['supplier_id'], unique=False)
    op.create_table('inventory_movements',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('inventory_id', sa.UUID(), nullable=False),
    sa.Column('movement_type', sa.Enum('purchase', 'sale', 'return', 'transfer_in', 'transfer_out', 'adjustment', name='inventory_movement_type'), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('reference_type', sa.String(length=50), nullable=True),
    sa.Column('reference_id', sa.UUID(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_movements_inventory_id'), 'inventory_movements', ['inventory_id'], unique=False)
    op.create_table('inventory_adjustments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('inventory_id', sa.UUID(), nullable=False),
    sa.Column('adjustment_type', sa.Enum('correction', 'damage', 'loss', 'found', name='inventory_adjustment_type'), nullable=False),
    sa.Column('quantity_change', sa.Integer(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('approved_by', sa.UUID(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_adjustments_inventory_id'), 'inventory_adjustments', ['inventory_id'], unique=False)
    op.create_table('inventory_reservations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('inventory_id', sa.UUID(), nullable=False),
    sa.Column('order_item_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('reserved', 'released', 'fulfilled', 'cancelled', name='inventory_reservation_status'), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_reservations_inventory_id'), 'inventory_reservations', ['inventory_id'], unique=False)
    op.create_index(op.f('ix_inventory_reservations_order_item_id'), 'inventory_reservations', ['order_item_id'], unique=True)
    op.create_foreign_key(None, 'inventories', 'warehouses', ['warehouse_id'], ['id'])
    op.create_foreign_key(None, 'inventories', 'products', ['product_id'], ['id'])
    op.create_foreign_key(None, 'inventory_movements', 'inventories', ['inventory_id'], ['id'])
    op.create_foreign_key(None, 'inventory_adjustments', 'inventories', ['inventory_id'], ['id'])
    op.create_foreign_key(None, 'inventory_adjustments', 'users', ['approved_by'], ['id'])
    op.create_foreign_key(None, 'inventory_reservations', 'inventories', ['inventory_id'], ['id'])
    op.create_foreign_key(None, 'inventory_reservations', 'order_items', ['order_item_id'], ['id'])
    op.create_foreign_key(None, 'product_suppliers', 'products', ['product_id'], ['id'])
    op.create_foreign_key(None, 'product_suppliers', 'suppliers', ['supplier_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'product_suppliers', type_='foreignkey')
    op.drop_constraint(None, 'product_suppliers', type_='foreignkey')
    op.drop_constraint(None, 'inventory_reservations', type_='foreignkey')
    op.drop_constraint(None, 'inventory_reservations', type_='foreignkey')
    op.drop_constraint(None, 'inventory_adjustments', type_='foreignkey')
    op.drop_constraint(None, 'inventory_adjustments', type_='foreignkey')
    op.drop_constraint(None, 'inventory_movements', type_='foreignkey')
    op.drop_constraint(None, 'inventories', type_='foreignkey')
    op.drop_constraint(None, 'inventories', type_='foreignkey')
    op.drop_index(op.f('ix_inventory_reservations_order_item_id'), table_name='inventory_reservations')
    op.drop_index(op.f('ix_inventory_reservations_inventory_id'), table_name='inventory_reservations')
    op.drop_table('inventory_reservations')
    op.drop_index(op.f('ix_inventory_adjustments_inventory_id'), table_name='inventory_adjustments')
    op.drop_table('inventory_adjustments')
    op.drop_index(op.f('ix_inventory_movements_inventory_id'), table_name='inventory_movements')
    op.drop_table('inventory_movements')
    op.drop_index(op.f('ix_product_suppliers_supplier_id'), table_name='product_suppliers')
    op.drop_index(op.f('ix_product_suppliers_product_id'), table_name='product_suppliers')
    op.drop_table('product_suppliers')
    op.drop_index(op.f('ix_inventories_warehouse_id'), table_name='inventories')
    op.drop_index(op.f('ix_inventories_product_id'), table_name='inventories')
    op.drop_table('inventories')
    op.drop_table('suppliers')
    op.drop_index(op.f('ix_warehouses_code'), table_name='warehouses')
    op.drop_table('warehouses')
