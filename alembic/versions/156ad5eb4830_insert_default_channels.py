"""insert default channels

Revision ID: 156ad5eb4830
Revises: 7fdc69da5822
Create Date: 2025-07-23 14:48:40.281932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '156ad5eb4830'
down_revision: Union[str, Sequence[str], None] = '7fdc69da5822'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy.sql import text

def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        INSERT INTO channels (name, description) VALUES
        ('Internal Medicine', 'Discussion on Internal Medicine'),
        ('General Surgery', 'Surgical discussions'),
        ('Neurology', 'Neurological cases')
        ON CONFLICT (name) DO NOTHING;
    """))


def downgrade():
    conn = op.get_bind()

    conn.execute(text("""
        DELETE FROM channels WHERE name IN (:name1, :name2, :name3)
    """), {
        "name1": "Internal Medicine",
        "name2": "Surgery",
        "name3": "Neurology"
    })
