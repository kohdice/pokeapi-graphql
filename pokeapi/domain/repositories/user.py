from abc import ABC, abstractmethod

from pokeapi.domain.entities.user import User as UserEntity
from pokeapi.infrastructure.database.models.users import User as UserModel


class UserRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for user repositories. Concrete implementations
    should inherit from this class and provide
    implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: UserModel) -> UserEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (UserModel): The SQLAlchemy model instance to be converted.

        Returns:
            UserEntity: The converted instance of the domain entity.

        """

        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, id_: int) -> UserEntity | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            UserEntity | None: The entity with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_username(self, username: str) -> UserEntity | None:
        """Retrieve an entity by its username.

        Args:
            username (str): The username of the entity to retrieve.

        Returns:
            UserEntity | None: The entity with the specified username, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, entity: UserEntity) -> UserEntity:
        """Create a new entity in the repository.

        Args:
            entity (UserEntity): The entity to be created.

        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, entity: UserEntity) -> UserEntity:
        """Update an existing entity in the repository.

        Args:
            entity (UserEntity): The entity to be updated.

        """
        pass  # pragma: no cover
