"""add_product_metadata_and_junction_tables

Revision ID: 9d0cdaec1e2e
Revises: fceaa055addd
Create Date: 2026-10-01 01:24:03.779414
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "9d0cdaec1e2e"
down_revision: str | None = "fceaa055addd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "skin_types",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_skin_types_name"), "skin_types", ["name"], unique=False)
    op.create_index(op.f("ix_skin_types_slug"), "skin_types", ["slug"], unique=True)
    op.create_index(
        op.f("ix_skin_types_is_active"), "skin_types", ["is_active"], unique=False
    )
    op.create_table(
        "skin_concerns",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_skin_concerns_name"), "skin_concerns", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_skin_concerns_slug"), "skin_concerns", ["slug"], unique=True
    )
    op.create_index(
        op.f("ix_skin_concerns_is_active"),
        "skin_concerns",
        ["is_active"],
        unique=False,
    )
    op.create_table(
        "ingredients",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingredients_name"), "ingredients", ["name"], unique=False)
    op.create_index(
        op.f("ix_ingredients_slug"), "ingredients", ["slug"], unique=True
    )
    op.create_index(
        op.f("ix_ingredients_is_active"), "ingredients", ["is_active"], unique=False
    )
    op.create_table(
        "benefits",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_benefits_name"), "benefits", ["name"], unique=False)
    op.create_index(op.f("ix_benefits_slug"), "benefits", ["slug"], unique=True)
    op.create_index(
        op.f("ix_benefits_is_active"), "benefits", ["is_active"], unique=False
    )
    op.create_table(
        "tags",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tags_name"), "tags", ["name"], unique=False)
    op.create_index(op.f("ix_tags_slug"), "tags", ["slug"], unique=True)
    op.create_index(
        op.f("ix_tags_is_active"), "tags", ["is_active"], unique=False
    )
    op.create_table(
        "routine_types",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_routine_types_name"), "routine_types", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_routine_types_slug"), "routine_types", ["slug"], unique=True
    )
    op.create_index(
        op.f("ix_routine_types_is_active"),
        "routine_types",
        ["is_active"],
        unique=False,
    )
    op.create_table(
        "product_skin_types",
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("skin_type_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name=op.f("product_skin_types_product_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["skin_type_id"],
            ["skin_types.id"],
            name=op.f("product_skin_types_skin_type_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "skin_type_id", name=op.f("uq_product_skin_type")
        ),
    )
    op.create_index(
        op.f("ix_product_skin_types_product_id"),
        "product_skin_types",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_skin_types_skin_type_id"),
        "product_skin_types",
        ["skin_type_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_skin_type_pair"),
        "product_skin_types",
        ["product_id", "skin_type_id"],
        unique=False,
    )
    op.create_table(
        "product_skin_concerns",
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("concern_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name=op.f("product_skin_concerns_product_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["concern_id"],
            ["skin_concerns.id"],
            name=op.f("product_skin_concerns_concern_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "concern_id", name=op.f("uq_product_skin_concern")
        ),
    )
    op.create_index(
        op.f("ix_product_skin_concerns_product_id"),
        "product_skin_concerns",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_skin_concerns_concern_id"),
        "product_skin_concerns",
        ["concern_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_skin_concern_pair"),
        "product_skin_concerns",
        ["product_id", "concern_id"],
        unique=False,
    )
    op.create_table(
        "product_ingredients",
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("ingredient_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name=op.f("product_ingredients_product_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
            name=op.f("product_ingredients_ingredient_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "ingredient_id", name=op.f("uq_product_ingredient")
        ),
    )
    op.create_index(
        op.f("ix_product_ingredients_product_id"),
        "product_ingredients",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_ingredients_ingredient_id"),
        "product_ingredients",
        ["ingredient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_ingredient_pair"),
        "product_ingredients",
        ["product_id", "ingredient_id"],
        unique=False,
    )
    op.create_table(
        "product_benefits",
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("benefit_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name=op.f("product_benefits_product_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["benefit_id"],
            ["benefits.id"],
            name=op.f("product_benefits_benefit_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "benefit_id", name=op.f("uq_product_benefit")
        ),
    )
    op.create_index(
        op.f("ix_product_benefits_product_id"),
        "product_benefits",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_benefits_benefit_id"),
        "product_benefits",
        ["benefit_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_benefit_pair"),
        "product_benefits",
        ["product_id", "benefit_id"],
        unique=False,
    )
    op.create_table(
        "product_tags",
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("tag_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name=op.f("product_tags_product_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tags.id"], name=op.f("product_tags_tag_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "tag_id", name=op.f("uq_product_tag")),
    )
    op.create_index(
        op.f("ix_product_tags_product_id"),
        "product_tags",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_tags_tag_id"),
        "product_tags",
        ["tag_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_tag_pair"),
        "product_tags",
        ["product_id", "tag_id"],
        unique=False,
    )
    op.create_table(
        "product_routines",
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("routine_type_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name=op.f("product_routines_product_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["routine_type_id"],
            ["routine_types.id"],
            name=op.f("product_routines_routine_type_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "routine_type_id", name=op.f("uq_product_routine")
        ),
    )
    op.create_index(
        op.f("ix_product_routines_product_id"),
        "product_routines",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_routines_routine_type_id"),
        "product_routines",
        ["routine_type_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_routine_pair"),
        "product_routines",
        ["product_id", "routine_type_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_product_routine_pair"), table_name="product_routines")
    op.drop_index(
        op.f("ix_product_routines_routine_type_id"), table_name="product_routines"
    )
    op.drop_index(
        op.f("ix_product_routines_product_id"), table_name="product_routines"
    )
    op.drop_table("product_routines")
    op.drop_index(op.f("ix_product_tag_pair"), table_name="product_tags")
    op.drop_index(op.f("ix_product_tags_tag_id"), table_name="product_tags")
    op.drop_index(op.f("ix_product_tags_product_id"), table_name="product_tags")
    op.drop_table("product_tags")
    op.drop_index(op.f("ix_product_benefit_pair"), table_name="product_benefits")
    op.drop_index(
        op.f("ix_product_benefits_benefit_id"), table_name="product_benefits"
    )
    op.drop_index(
        op.f("ix_product_benefits_product_id"), table_name="product_benefits"
    )
    op.drop_table("product_benefits")
    op.drop_index(op.f("ix_product_ingredient_pair"), table_name="product_ingredients")
    op.drop_index(
        op.f("ix_product_ingredients_ingredient_id"), table_name="product_ingredients"
    )
    op.drop_index(
        op.f("ix_product_ingredients_product_id"), table_name="product_ingredients"
    )
    op.drop_table("product_ingredients")
    op.drop_index(
        op.f("ix_product_skin_concern_pair"), table_name="product_skin_concerns"
    )
    op.drop_index(
        op.f("ix_product_skin_concerns_concern_id"), table_name="product_skin_concerns"
    )
    op.drop_index(
        op.f("ix_product_skin_concerns_product_id"), table_name="product_skin_concerns"
    )
    op.drop_table("product_skin_concerns")
    op.drop_index(op.f("ix_product_skin_type_pair"), table_name="product_skin_types")
    op.drop_index(
        op.f("ix_product_skin_types_skin_type_id"), table_name="product_skin_types"
    )
    op.drop_index(
        op.f("ix_product_skin_types_product_id"), table_name="product_skin_types"
    )
    op.drop_table("product_skin_types")
    op.drop_index(
        op.f("ix_routine_types_is_active"), table_name="routine_types"
    )
    op.drop_index(op.f("ix_routine_types_slug"), table_name="routine_types")
    op.drop_index(op.f("ix_routine_types_name"), table_name="routine_types")
    op.drop_table("routine_types")
    op.drop_index(op.f("ix_tags_is_active"), table_name="tags")
    op.drop_index(op.f("ix_tags_slug"), table_name="tags")
    op.drop_index(op.f("ix_tags_name"), table_name="tags")
    op.drop_table("tags")
    op.drop_index(op.f("ix_benefits_is_active"), table_name="benefits")
    op.drop_index(op.f("ix_benefits_slug"), table_name="benefits")
    op.drop_index(op.f("ix_benefits_name"), table_name="benefits")
    op.drop_table("benefits")
    op.drop_index(
        op.f("ix_ingredients_is_active"), table_name="ingredients"
    )
    op.drop_index(op.f("ix_ingredients_slug"), table_name="ingredients")
    op.drop_index(op.f("ix_ingredients_name"), table_name="ingredients")
    op.drop_table("ingredients")
    op.drop_index(
        op.f("ix_skin_concerns_is_active"), table_name="skin_concerns"
    )
    op.drop_index(op.f("ix_skin_concerns_slug"), table_name="skin_concerns")
    op.drop_index(op.f("ix_skin_concerns_name"), table_name="skin_concerns")
    op.drop_table("skin_concerns")
    op.drop_index(
        op.f("ix_skin_types_is_active"), table_name="skin_types"
    )
    op.drop_index(op.f("ix_skin_types_slug"), table_name="skin_types")
    op.drop_index(op.f("ix_skin_types_name"), table_name="skin_types")
    op.drop_table("skin_types")
