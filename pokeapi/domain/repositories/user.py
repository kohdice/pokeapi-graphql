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
    def get_by_nickname(self, nickname: str) -> BaseEntity | None:
        """Retrieve an entity by its nickname.

        Args:
            nickname (str): The nickname of the entity to retrieve.

        Returns:
            BaseEntity | None: The entity with the specified nickname, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, entity: BaseEntity) -> BaseEntity:
        """Create a new entity in the repository.

        Args:
            entity (BaseEntity): The entity to be created.

        Returns:
            BaseEntity: The created entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, entity: BaseEntity) -> BaseEntity:
        """Update an existing entity in the repository.

        Args:
            entity (BaseEntity): The entity to be updated.

        Returns:
            BaseEntity: The updated entity.

        """
        pass  # pragma: no cover
