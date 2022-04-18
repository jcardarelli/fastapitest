"""Add content column to posts table

Revision ID: 696c1737f2b7
Revises: c92c631d309b
Create Date: 2022-04-17 19:04:23.050126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "696c1737f2b7"
down_revision = "c92c631d309b"
branch_labels = None
depends_on = None


def upgrade():
    """upgrade command"""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    """downgrade command"""
    op.drop_column("posts", "content")
    pass
