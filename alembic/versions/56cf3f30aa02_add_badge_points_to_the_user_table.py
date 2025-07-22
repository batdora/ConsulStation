"""add badge points to the user table

Revision ID: 56cf3f30aa02
Revises: c279faea4e43
Create Date: 2025-07-22 16:11:54.714581

"""
from typing import Sequence, Union

from alembic import op
from psycopg import Column
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56cf3f30aa02'
down_revision: Union[str, Sequence[str], None] = 'c279faea4e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('badge_points', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('users', 'badge_points')
