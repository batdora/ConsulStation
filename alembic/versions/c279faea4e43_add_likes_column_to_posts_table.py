"""Add likes column to posts table

Revision ID: c279faea4e43
Revises: 686ad0ecc30e
Create Date: 2025-07-14 15:35:51.964645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c279faea4e43'
down_revision: Union[str, Sequence[str], None] = '686ad0ecc30e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('likes', sa.Integer(), nullable=False, server_default='0')
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'likes')
    pass
