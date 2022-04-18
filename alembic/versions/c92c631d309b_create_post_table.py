"""Create post table

Revision ID: c92c631d309b
Revises:
Create Date: 2022-04-17 18:58:17.322628

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c92c631d309b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    upgrade doc string
    """
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    """
    downgrade doc string
    """
    op.drop_table("posts")
