"""create token_whitelist table

Revision ID: dbd17ec698c8
Revises: ae489317139c
Create Date: 2024-02-27 22:05:34.681269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dbd17ec698c8"
down_revision: Union[str, None] = "ae489317139c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("token_whitelist",
    sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="ID"),
    sa.Column("user_id", sa.Integer(), nullable=False, comment="User's ID"),
    sa.Column("access_token", sa.String(length=36), nullable=False, comment="Access Token"),
    sa.Column("refresh_token", sa.String(length=36), nullable=False, comment="Refresh Token"),
    sa.Column("created_by", sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column("created_at", sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column("updated_by", sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table("token_whitelist")
