"""merge multiple heads

Revision ID: 5f5a2ed5fc92
Revises: 28a4f978cc5d, a1b2c3d4e5f6, d5e6f7a8b9c0, f6a7b8c9d0e1
Create Date: 2026-09-19 21:52:19.638412
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "5f5a2ed5fc92"
down_revision: Union[str, None] = (
    "28a4f978cc5d",
    "a1b2c3d4e5f6",
    "d5e6f7a8b9c0",
    "f6a7b8c9d0e1",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
