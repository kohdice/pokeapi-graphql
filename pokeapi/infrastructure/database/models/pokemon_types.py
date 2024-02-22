from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .pokemon_mst import Pokemon
    from .type_mst import TypeMst


class PokemonTypes(BaseModel, TimestampMixin):
    """Class that maps to the `pokemon_types` table."""

    __tablename__ = "pokemon_types"

    pokemon_id: Mapped[int] = mapped_column(
        ForeignKey("pokemon_mst.id"), primary_key=True
    )
    type_id: Mapped[int] = mapped_column(ForeignKey("type_mst.id"), primary_key=True)
    slot: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # Relationships
    pokemon: Mapped[Pokemon] = relationship("Pokemon", back_populates="pokemon_types")
    type_: Mapped[TypeMst] = relationship("TypeMst", back_populates="pokemon_types")
