from sqlalchemy.orm import DeclarativeBase

from pokeapi.infrastructure.database.models.mixins import TimestampMixin


class BaseModel(DeclarativeBase, TimestampMixin):
    """Base class for all SQLAlchemy models."""
