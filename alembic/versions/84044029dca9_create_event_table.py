"""create event table

Revision ID: 84044029dca9
Revises: 6702242cd39f
Create Date: 2023-08-02 20:12:05.290846

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "84044029dca9"
down_revision = "6702242cd39f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("aggregate_id", sa.String(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column("meta_data", sa.JSON(), nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("aggregate_name", sa.String(), nullable=True),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade():
    op.drop_table("events")
