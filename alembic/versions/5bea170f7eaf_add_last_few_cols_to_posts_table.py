"""Add last few cols to posts table

Revision ID: 5bea170f7eaf
Revises: e1db23a4ae9a
Create Date: 2022-04-17 19:21:19.584975

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5bea170f7eaf"
down_revision = "e1db23a4ae9a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
