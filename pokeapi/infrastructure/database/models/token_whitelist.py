from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .users import User


class TokenWhitelist(BaseModel, TimestampMixin):
    """Class that maps to the token_whitelist table."""

    __tablename__ = "token_whitelist"

    id_: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    access_token: Mapped[str] = mapped_column(String(36), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(36), nullable=False)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="token_whitelist")
