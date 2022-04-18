"""Add user table

Revision ID: 9dc05a7190bc
Revises: 696c1737f2b7
Create Date: 2022-04-17 19:07:01.543857

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9dc05a7190bc"
down_revision = "696c1737f2b7"
branch_labels = None
depends_on = None


def upgrade():
    """upgrade command"""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    """downgrade command"""
    pass
