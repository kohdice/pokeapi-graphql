"""create users table

Revision ID: ae489317139c
Revises: a02206b606d9
Create Date: 2024-02-27 21:48:50.790664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae489317139c"
down_revision: Union[str, None] = "a02206b606d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
    sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="ID"),
    sa.Column("username", sa.String(length=30), nullable=False, unique=True, comment="Username"),
    sa.Column("password", sa.String(length=255), nullable=False, comment="Password"),
    sa.Column("created_by", sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column("created_at", sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column("updated_by", sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.PrimaryKeyConstraint("id"),
    ),


def downgrade() -> None:
    op.drop_table("users")
