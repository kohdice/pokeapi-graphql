from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity


class PokemonServiceABC(ABC):
    """Abstract base class for Pokémon services.

    This class defines the interface for Pokémon services. Concrete implementations should
    inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def get_by_id(self, id_: int) -> BaseEntity | None:
        """Retrieve a Pokémon by its identifier.

        Args:
            id_ (int): The identifier of the Pokémon to retrieve.

        Returns:
            BaseEntity | None: The Pokémon with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list | list[BaseEntity]:
        """Retrieve all pokemon from the repository.

        Returns:
            list | list[BaseEntity]: A list of all Pokémon in the repository.

        """
        pass  # pragma: no cover
