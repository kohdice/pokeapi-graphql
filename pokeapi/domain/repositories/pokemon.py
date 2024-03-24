from abc import ABC, abstractmethod

from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.infrastructure.database.models import Pokemon as PokemonModel


class PokemonRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for pokemon repositories. Concrete implementations
    should inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: PokemonModel) -> PokemonEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (BaseModel): The SQLAlchemy model instance to be converted.

        Returns:
            Pokemon: The converted instance of the domain entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, id_: int) -> PokemonEntity | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            Pokemon | None: The entity with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_pokedex_number(self, pokedex_number: int) -> PokemonEntity | None:
        """Retrieve an entity by its pokedex number.

        Args:
            pokedex_number (int): The pokedex number of the entity to retrieve.

        Returns:
            Pokemon | None: The entity with the specified pokedex number, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_name(self, name: str) -> PokemonEntity | None:
        """Retrieve an entity by its name.

        Args:
            name (str): The name of the entity to retrieve.

        Returns:
            Pokemon | None: The entity with the specified name, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[PokemonEntity]:
        """Retrieve all entities from the repository.

        Returns:
            list[Pokemon]: A list of all entities in the repository.

        """
        pass  # pragma: no cover
