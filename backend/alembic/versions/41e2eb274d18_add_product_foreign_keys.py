"""alter product fk columns to uuid and add foreign keys

Revision ID: 41e2eb274d18
Revises: 0eb2b70ebe7f
Create Date: 2026-09-17 05:03:45.024293
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "41e2eb274d18"
down_revision: str | None = "0eb2b70ebe7f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.alter_column(
            "brand_id",
            existing_type=sa.String(length=36),
            type_=sa.UUID(),
            existing_nullable=False,
            postgresql_using="brand_id::uuid",
        )
        batch_op.alter_column(
            "category_id",
            existing_type=sa.String(length=36),
            type_=sa.UUID(),
            existing_nullable=False,
            postgresql_using="category_id::uuid",
        )

    with op.batch_alter_table("product_images", schema=None) as batch_op:
        batch_op.alter_column(
            "product_id",
            existing_type=sa.String(length=36),
            type_=sa.UUID(),
            existing_nullable=False,
            postgresql_using="product_id::uuid",
        )

    with op.batch_alter_table("product_variants", schema=None) as batch_op:
        batch_op.alter_column(
            "product_id",
            existing_type=sa.String(length=36),
            type_=sa.UUID(),
            existing_nullable=False,
            postgresql_using="product_id::uuid",
        )

    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.alter_column(
            "parent_id",
            existing_type=sa.String(length=36),
            type_=sa.UUID(),
            existing_nullable=True,
            postgresql_using="parent_id::uuid",
        )

    op.create_foreign_key(None, "categories", "categories", ["parent_id"], ["id"])
    op.create_foreign_key(None, "product_images", "products", ["product_id"], ["id"])
    op.create_foreign_key(None, "product_variants", "products", ["product_id"], ["id"])
    op.create_foreign_key(None, "products", "brands", ["brand_id"], ["id"])
    op.create_foreign_key(None, "products", "categories", ["category_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_constraint(None, "product_variants", type_="foreignkey")
    op.drop_constraint(None, "product_images", type_="foreignkey")
    op.drop_constraint(None, "categories", type_="foreignkey")

    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.alter_column(
            "parent_id",
            existing_type=sa.UUID(),
            type_=sa.String(length=36),
            existing_nullable=True,
            postgresql_using="parent_id::text",
        )

    with op.batch_alter_table("product_variants", schema=None) as batch_op:
        batch_op.alter_column(
            "product_id",
            existing_type=sa.UUID(),
            type_=sa.String(length=36),
            existing_nullable=False,
            postgresql_using="product_id::text",
        )

    with op.batch_alter_table("product_images", schema=None) as batch_op:
        batch_op.alter_column(
            "product_id",
            existing_type=sa.UUID(),
            type_=sa.String(length=36),
            existing_nullable=False,
            postgresql_using="product_id::text",
        )

    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.alter_column(
            "category_id",
            existing_type=sa.UUID(),
            type_=sa.String(length=36),
            existing_nullable=False,
            postgresql_using="category_id::text",
        )
        batch_op.alter_column(
            "brand_id",
            existing_type=sa.UUID(),
            type_=sa.String(length=36),
            existing_nullable=False,
            postgresql_using="brand_id::text",
        )
