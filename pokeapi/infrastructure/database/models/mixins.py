import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin class that adds timestamp columns to a model."""

    created_by: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
    updated_by: Mapped[str] = mapped_column(String(30), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
        onupdate=datetime.datetime.now,
    )
    deleted_at: Mapped[datetime.datetime]
