"""add event type column

Revision ID: 0a2b416137f9
Revises: 84044029dca9
Create Date: 2023-08-26 21:58:15.087301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a2b416137f9'
down_revision = '84044029dca9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column("event_type", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("events", "event_type")
