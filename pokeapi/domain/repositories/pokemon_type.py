from abc import ABC, abstractmethod

from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.infrastructure.database.models import TypeMst


class TypeRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for type repositories. Concrete implementations
    should inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: TypeMst) -> PokemonType:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (TypeMst): The SQLAlchemy model instance to be converted.

        Returns:
            PokemonType: The converted instance of the domain entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, id_: int) -> PokemonType | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            PokemonType | None: The entity with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[PokemonType]:
        """Retrieve all entities from the repository.

        Returns:
            list[PokemonType]: A list of all entities in the repository.

        """
        pass  # pragma: no cover
