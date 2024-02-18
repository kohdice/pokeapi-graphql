from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pokeapi.infrastructure.database.db import Base

from .mixins import TimestampMixin


class AbilityMst(Base, TimestampMixin):
    """Class that maps to the `ability_mst` table."""

    __tablename__ = "ability_mst"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    ability: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    pokemon_abilities = relationship("PokemonAbilities", back_populates="ability")
