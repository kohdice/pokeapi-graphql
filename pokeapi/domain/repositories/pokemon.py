from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.infrastructure.database.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=BaseEntity)


class PokemonRepositoryABC(Generic[T, U], ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for pokemon repositories. Concrete implementations
    should inherit from this class and provide implementations for the abstract methods.

    Attributes:
        db (Session): The database session object used by the repository.

    """

    @abstractmethod
    def __init__(self, db: Session) -> None:
        """Initializer for PokemonRepository.

        Args:
            db (Session): The database session object used by the repository.

        """
        self._db = db

    @abstractmethod
    def _convert_to_entity(self, model: T) -> U:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (T): The SQLAlchemy model instance to be converted.

        Returns:
            U: The converted instance of the domain entity.

        """
        ...  # pragma: no cover

    @abstractmethod
    def get_by_id(self, id_: int) -> U | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            U | None: The entity with the specified identifier, or None if not found.

        """
        ...  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list | list[U]:
        """Retrieve all entities from the repository.

        Returns:
            list | list[U]: A list of all entities in the repository.

        """
        ...  # pragma: no cover
