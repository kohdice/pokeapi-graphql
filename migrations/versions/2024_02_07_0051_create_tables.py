"""create tables

Revision ID: a02206b606d9
Revises:
Create Date: 2024-02-07 00:51:02.387899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from migrations.seeds.ability_mst import ability_mst_seed
from migrations.seeds.pokemon_abilities import pokemon_abilities_seed
from migrations.seeds.pokemon_mst import pokemon_mst_seed
from migrations.seeds.pokemon_types import pokemon_types_seed
from migrations.seeds.type_mst import type_mst_seed


# revision identifiers, used by Alembic.
revision: str = 'a02206b606d9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    ability_mst = op.create_table('ability_mst',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment="ID"),
    sa.Column('ability', sa.String(length=100), nullable=False, comment="Ability"),
    sa.Column('created_by', sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column('updated_by', sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.PrimaryKeyConstraint('id')
    )
    pokemon_mst = op.create_table('pokemon_mst',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment="ID"),
    sa.Column('national_pokedex_number', sa.Integer(), nullable=False, comment="National Pokédex Number"),
    sa.Column('name', sa.String(length=255), nullable=False, comment="Name"),
    sa.Column('hp', sa.SmallInteger(), nullable=False, comment="HP"),
    sa.Column('attack', sa.SmallInteger(), nullable=False, comment="Attack"),
    sa.Column('defense', sa.SmallInteger(), nullable=False, comment="Defense"),
    sa.Column('special_attack', sa.SmallInteger(), nullable=False, comment="Special Attack"),
    sa.Column('special_defense', sa.SmallInteger(), nullable=False, comment="Special Defense"),
    sa.Column('speed', sa.SmallInteger(), nullable=False, comment="Speed"),
    sa.Column('base_total', sa.SmallInteger(), nullable=False, comment="Base Total"),
    sa.Column('created_by', sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column('updated_by', sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.PrimaryKeyConstraint('id')
    )
    type_mst = op.create_table('type_mst',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment="ID"),
    sa.Column('type', sa.String(length=50), nullable=False, comment="Type"),
    sa.Column('created_by', sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column('updated_by', sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.PrimaryKeyConstraint('id')
    )
    pokemon_abilities = op.create_table('pokemon_abilities',
    sa.Column('pokemon_id', sa.Integer(), nullable=False, comment="Pokemon ID"),
    sa.Column('ability_id', sa.Integer(), nullable=False, comment="Ability ID"),
    sa.Column('slot', sa.SmallInteger(), nullable=False, comment="Slot of Ability"),
    sa.Column('is_hidden', sa.Boolean(), nullable=False, comment="Hidden Ability or Not"),
    sa.Column('created_by', sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column('updated_by', sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.ForeignKeyConstraint(['ability_id'], ['ability_mst.id'], ),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon_mst.id'], ),
    sa.PrimaryKeyConstraint('pokemon_id', 'ability_id')
    )
    pokemon_types = op.create_table('pokemon_types',
    sa.Column('pokemon_id', sa.Integer(), nullable=False, comment="Pokemon ID"),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('slot', sa.SmallInteger(), nullable=False),
    sa.Column('created_by', sa.String(length=30), nullable=False, comment="Creator"),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment="Creation DateTime"),
    sa.Column('updated_by', sa.String(length=30), nullable=False, comment="Updater"),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment="Update DateTime"),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Deletion DateTime"),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon_mst.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['type_mst.id'], ),
    sa.PrimaryKeyConstraint('pokemon_id', 'type_id')
    )
    # Seed data insertion
    op.bulk_insert(ability_mst, ability_mst_seed)
    op.bulk_insert(pokemon_mst, pokemon_mst_seed)
    op.bulk_insert(type_mst, type_mst_seed)
    op.bulk_insert(pokemon_abilities, pokemon_abilities_seed)
    op.bulk_insert(pokemon_types, pokemon_types_seed)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_types')
    op.drop_table('pokemon_abilities')
    op.drop_table('type_mst')
    op.drop_table('pokemon_mst')
    op.drop_table('ability_mst')
    # ### end Alembic commands ###
