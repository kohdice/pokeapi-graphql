from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .token_whitelist import TokenWhitelist


class User(BaseModel, TimestampMixin):
    """Class that maps to the `users` table."""

    __tablename__ = "users"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    token_whitelist: Mapped[list[TokenWhitelist]] = relationship(
        "TokenWhitelist", back_populates="user"
    )
