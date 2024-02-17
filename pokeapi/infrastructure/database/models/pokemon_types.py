from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pokeapi.infrastructure.database.db import Base

from .mixins import TimestampMixin


class PokemonTypes(Base, TimestampMixin):
    """Class that maps to the `pokemon_types` table."""

    __tablename__ = "pokemon_types"

    pokemon_id: Mapped[int] = mapped_column(
        ForeignKey("pokemon_mst.id"), primary_key=True
    )
    type_id: Mapped[int] = mapped_column(ForeignKey("type_mst.id"), primary_key=True)
    slot: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # Relationships
    pokemon: Mapped["Pokemon"] = relationship(  # noqa: F821
        "Pokemon", back_populates="pokemon_types"
    )
    type_: Mapped["TypeMst"] = relationship(  # noqa: F821
        "TypeMst", back_populates="pokemon_types"
    )
