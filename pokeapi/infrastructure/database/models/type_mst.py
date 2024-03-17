from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .pokemon_types import PokemonTypes


class TypeMst(BaseModel, TimestampMixin):
    """Class that maps to the `type_mst` table."""

    __tablename__ = "type_mst"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    type_: Mapped[str] = mapped_column("type", String(50), nullable=False)

    # Relationships
    pokemon_types: Mapped[list[PokemonTypes]] = relationship(
        "PokemonTypes", back_populates="type_"
    )
