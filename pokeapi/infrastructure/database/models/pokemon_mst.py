from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .pokemon_abilities import PokemonAbilities
    from .pokemon_types import PokemonTypes


class Pokemon(BaseModel, TimestampMixin):
    """Class that maps to the `pokemon_mst` table."""

    __tablename__ = "pokemon_mst"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    national_pokedex_number: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hp: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    attack: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    defense: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    special_attack: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    special_defense: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    speed: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    base_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # Relationships
    pokemon_types: Mapped[list[PokemonTypes]] = relationship(
        "PokemonTypes", back_populates="pokemon"
    )
    pokemon_abilities: Mapped[list[PokemonAbilities]] = relationship(
        "PokemonAbilities", back_populates="pokemon"
    )
