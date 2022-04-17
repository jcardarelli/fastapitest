"""Add content column to posts table

Revision ID: 2c51d2111249
Revises: fd3becef14f9
Create Date: 2022-04-17 16:00:14.608282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2c51d2111249"
down_revision = "fd3becef14f9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
