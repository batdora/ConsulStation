"""Add foreign key to posts table

Revision ID: c89d33445249
Revises: 1172d789e8a2
Create Date: 2025-07-07 16:24:14.202962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c89d33445249'
down_revision: Union[str, Sequence[str], None] = '1172d789e8a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'fk_posts_owner_id_users',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
        )
    pass


def downgrade() -> None:
    op.drop_constraint(
        'fk_posts_owner_id_users',
        table_name='posts'
    )
    op.drop_column('posts', 'owner_id')
    pass
