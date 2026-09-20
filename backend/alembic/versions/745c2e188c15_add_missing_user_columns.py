"""add missing user columns

Revision ID: 745c2e188c15
Revises: 5f5a2ed5fc92
Create Date: 2026-09-19 21:56:00.709492
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '745c2e188c15'
down_revision: Union[str, None] = '5f5a2ed5fc92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('locked_until', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'locked_until')
    op.drop_column('users', 'failed_login_attempts')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'is_verified')
