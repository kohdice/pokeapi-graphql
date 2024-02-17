from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pokeapi.infrastructure.database.db import Base

from .mixins import TimestampMixin


class TypeMst(Base, TimestampMixin):
    """Class that maps to the `type_mst` table."""

    __tablename__ = "type_mst"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    type_: Mapped[str] = mapped_column("type", String(50), nullable=False)

    # Relationships
    pokemon_types: Mapped[list["PokemonTypes"]] = relationship(  # noqa: F821
        "PokemonTypes", back_populates="type_"
    )
