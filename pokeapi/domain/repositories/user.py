from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.infrastructure.database.models.base import BaseModel


class UserRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for user repositories. Concrete implementations
    should inherit from this class and provide
    implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: BaseModel) -> BaseEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (BaseModel): The SQLAlchemy model instance to be converted.

        Returns:
            BaseEntity: The converted instance of the domain entity.

        """

        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, id_: int) -> BaseEntity | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            BaseEntity | None: The entity with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_username(self, username: str) -> BaseEntity | None:
        """Retrieve an entity by its username.

        Args:
            username (str): The username of the entity to retrieve.

        Returns:
            BaseEntity | None: The entity with the specified username, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, entity: BaseEntity) -> None:
        """Create a new entity in the repository.

        Args:
            entity (BaseEntity): The entity to be created.

        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, entity: BaseEntity) -> None:
        """Update an existing entity in the repository.

        Args:
            entity (BaseEntity): The entity to be updated.

        """
        pass  # pragma: no cover
