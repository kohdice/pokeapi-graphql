from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.infrastructure.database.models.base import BaseModel


class PokemonRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for pokemon repositories. Concrete implementations
    should inherit from this class and provide implementations for the abstract methods.

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
    def get_all(self) -> list | list[BaseEntity]:
        """Retrieve all entities from the repository.

        Returns:
            list | list[BaseEntity]: A list of all entities in the repository.

        """
        pass  # pragma: no cover
