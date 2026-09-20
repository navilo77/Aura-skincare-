"""add cart wishlist profile email verification tables

Revision ID: a1b2c3d4e5f7
Revises: feb39ceece7d
Create Date: 2026-09-19 03:30:00.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'a1b2c3d4e5f7'
down_revision: str | None = 'feb39ceece7d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('carts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_carts_user_id'), 'carts', ['user_id'], unique=False)
    op.create_table('cart_items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('cart_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('product_variant_id', sa.UUID(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('subtotal', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_items_cart_id'), 'cart_items', ['cart_id'], unique=False)
    op.create_index(op.f('ix_cart_items_product_id'), 'cart_items', ['product_id'], unique=False)
    op.create_index(op.f('ix_cart_items_product_variant_id'), 'cart_items', ['product_variant_id'], unique=False)
    op.create_foreign_key(None, 'cart_items', 'carts', ['cart_id'], ['id'])
    op.create_foreign_key(None, 'cart_items', 'products', ['product_id'], ['id'])
    op.create_foreign_key(None, 'cart_items', 'product_variants', ['product_variant_id'], ['id'])
    op.create_table('wishlists',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wishlists_user_id'), 'wishlists', ['user_id'], unique=False)
    op.create_table('wishlist_items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('wishlist_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('product_variant_id', sa.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wishlist_items_wishlist_id'), 'wishlist_items', ['wishlist_id'], unique=False)
    op.create_index(op.f('ix_wishlist_items_product_id'), 'wishlist_items', ['product_id'], unique=False)
    op.create_index(op.f('ix_wishlist_items_product_variant_id'), 'wishlist_items', ['product_variant_id'], unique=False)
    op.create_foreign_key(None, 'wishlist_items', 'wishlists', ['wishlist_id'], ['id'])
    op.create_foreign_key(None, 'wishlist_items', 'products', ['product_id'], ['id'])
    op.create_foreign_key(None, 'wishlist_items', 'product_variants', ['product_variant_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'wishlist_items', type_='foreignkey')
    op.drop_constraint(None, 'wishlist_items', type_='foreignkey')
    op.drop_constraint(None, 'wishlist_items', type_='foreignkey')
    op.drop_index(op.f('ix_wishlist_items_product_variant_id'), table_name='wishlist_items')
    op.drop_index(op.f('ix_wishlist_items_product_id'), table_name='wishlist_items')
    op.drop_index(op.f('ix_wishlist_items_wishlist_id'), table_name='wishlist_items')
    op.drop_table('wishlist_items')
    op.drop_constraint(None, 'carts', type_='foreignkey')
    op.drop_constraint(None, 'carts', type_='foreignkey')
    op.drop_constraint(None, 'carts', type_='foreignkey')
    op.drop_index(op.f('ix_cart_items_product_variant_id'), table_name='cart_items')
    op.drop_index(op.f('ix_cart_items_product_id'), table_name='cart_items')
    op.drop_index(op.f('ix_cart_items_cart_id'), table_name='cart_items')
    op.drop_table('cart_items')
    op.drop_index(op.f('ix_wishlists_user_id'), table_name='wishlists')
    op.drop_table('wishlists')
    op.drop_index(op.f('ix_carts_user_id'), table_name='carts')
    op.drop_table('carts')
