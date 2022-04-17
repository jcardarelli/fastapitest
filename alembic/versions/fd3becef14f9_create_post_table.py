"""Create post table

Revision ID: fd3becef14f9
Revises:
Create Date: 2022-04-16 20:20:42.124890

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "fd3becef14f9"
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
