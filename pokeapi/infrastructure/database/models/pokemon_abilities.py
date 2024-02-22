from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .ability_mst import AbilityMst
    from .pokemon_mst import Pokemon


class PokemonAbilities(BaseModel, TimestampMixin):
    """Class that maps to the `pokemon_abilities` table."""

    __tablename__ = "pokemon_abilities"

    pokemon_id: Mapped[int] = mapped_column(
        ForeignKey("pokemon_mst.id"), primary_key=True
    )
    ability_id: Mapped[int] = mapped_column(
        ForeignKey("ability_mst.id"), primary_key=True
    )
    slot: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Relationships
    pokemon: Mapped[Pokemon] = relationship(
        "Pokemon", back_populates="pokemon_abilities"
    )
    ability: Mapped[AbilityMst] = relationship(
        "AbilityMst", back_populates="pokemon_abilities"
    )
