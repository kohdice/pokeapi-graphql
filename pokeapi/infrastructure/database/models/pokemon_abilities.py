from sqlalchemy import Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pokeapi.infrastructure.database.models.base import BaseModel


class PokemonAbilities(BaseModel):
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
    pokemon = relationship("Pokemon", back_populates="pokemon_abilities")
    ability = relationship("AbilityMst", back_populates="pokemon_abilities")
