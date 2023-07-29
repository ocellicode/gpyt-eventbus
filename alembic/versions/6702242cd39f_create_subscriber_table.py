"""create subscriber table

Revision ID: 6702242cd39f
Revises:
Create Date: 2023-07-29 15:55:46.919377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6702242cd39f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "subscriber",
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("url")
    )


def downgrade():
    op.drop_table("subscriber")
