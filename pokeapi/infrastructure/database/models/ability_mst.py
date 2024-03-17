from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .pokemon_abilities import PokemonAbilities


class AbilityMst(BaseModel, TimestampMixin):
    """Class that maps to the `ability_mst` table."""

    __tablename__ = "ability_mst"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    ability: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    pokemon_abilities: Mapped[list[PokemonAbilities]] = relationship(
        "PokemonAbilities", back_populates="ability"
    )
