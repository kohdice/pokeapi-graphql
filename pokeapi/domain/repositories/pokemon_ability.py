from abc import ABC, abstractmethod

from pokeapi.domain.entities.pokemon_ability import PokemonAbility
from pokeapi.infrastructure.database.models import AbilityMst


class AbilityRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for ability repositories. Concrete implementations
    should inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: AbilityMst) -> PokemonAbility:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (AbilityMst): The SQLAlchemy model instance to be converted.

        Returns:
            PokemonAbility: The converted instance of the domain entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_id(self, id_: int) -> PokemonAbility | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            PokemonAbility | None: The entity with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[PokemonAbility]:
        """Retrieve all entities from the repository.

        Returns:
            list[PokemonAbility]: A list of all entities in the repository.

        """
        pass  # pragma: no cover
