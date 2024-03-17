from abc import ABC, abstractmethod

from pokeapi.domain.entities.pokemon import Pokemon


class PokemonServiceABC(ABC):
    """Abstract base class for Pokémon services.

    This class defines the interface for Pokémon services. Concrete implementations should
    inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def get_by_id(self, id_: int) -> Pokemon | None:
        """Retrieve a Pokémon by its identifier.

        Args:
            id_ (int): The identifier of the Pokémon to retrieve.

        Returns:
            Pokemon | None: The Pokémon with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[Pokemon]:
        """Retrieve all Pokémon from the repository.

        Returns:
            list[Pokemon]: A list of all Pokémon in the repository.

        """
        pass  # pragma: no cover
