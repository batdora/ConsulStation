"""Create votes table

Revision ID: c9720f724e57
Revises: 14d79569220f
Create Date: 2025-07-13 16:15:00.965189

"""
from typing import Sequence, Union

from alembic import op
from psycopg import Column
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9720f724e57'
down_revision: Union[str, Sequence[str], None] = '14d79569220f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'votes',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('like_by_owner', sa.Boolean(), default=False, nullable=False)  # Indicates if the root post owner liked the reply
    )
    op.create_foreign_key(
        'fk_votes_post_id_posts',
        source_table='votes',
        referent_table='posts',
        local_cols=['post_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_votes_user_id_users',
        source_table='votes',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass

def downgrade() -> None:
    op.drop_constraint('fk_votes_post_id_posts', 'votes', type_='foreignkey')
    op.drop_constraint('fk_votes_user_id_users', 'votes', type_='foreignkey')
    op.drop_table('votes')  