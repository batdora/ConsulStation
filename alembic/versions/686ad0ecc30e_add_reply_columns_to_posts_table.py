"""Add reply columns to posts table

Revision ID: 686ad0ecc30e
Revises: c9720f724e57
Create Date: 2025-07-14 14:27:27.545744

"""
from operator import add
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '686ad0ecc30e'
down_revision: Union[str, Sequence[str], None] = 'c9720f724e57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('direct_reply_count', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column(
        'posts',
        sa.Column('total_reply_count', sa.Integer(), nullable=False, server_default='0')
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'direct_reply_count')
    op.drop_column('posts', 'total_reply_count')
    pass
