from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    __abstract__ = True
