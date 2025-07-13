"""Create posts table

Revision ID: 14d79569220f
Revises: 9bf51109d0ec
Create Date: 2025-07-13 16:14:19.775277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14d79569220f'
down_revision: Union[str, Sequence[str], None] = '9bf51109d0ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('published', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('reply_to', sa.Integer(), nullable=True), # Allow None for root posts
        sa.Column('original_post_owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'fk_posts_owner_id_users',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
        )
    op.create_foreign_key(
        'fk_posts_reply_to_posts',
        source_table='posts',
        referent_table='posts',
        local_cols=['reply_to'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_posts_original_post_owner_id_users',
        source_table='posts',
        referent_table='users',
        local_cols=['original_post_owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('fk_posts_owner_id_users', 'posts', type_='foreignkey')
    op.drop_constraint('fk_posts_reply_to_posts', 'posts', type_='foreignkey')
    op.drop_constraint('fk_posts_original_post_owner_id_users', 'posts', type_='foreignkey')
    op.drop_table('posts')
    pass
