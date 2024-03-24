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
    def get_by_pokedex_number(self, pokedex_number: int) -> Pokemon | None:
        """Retrieve a Pokémon by its Pokédex number.

        Args:
            pokedex_number (int): The Pokédex number of the Pokémon to retrieve.

        Returns:
            Pokemon | None: The Pokémon with the specified Pokédex number, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_name(self, name: str) -> Pokemon | None:
        """Retrieve a Pokémon by its name.

        Args:
            name (str): The name of the Pokémon to retrieve.

        Returns:
            Pokemon | None: The Pokémon with the specified name, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[Pokemon]:
        """Retrieve all Pokémon from the repository.

        Returns:
            list[Pokemon]: A list of all Pokémon in the repository.

        """
        pass  # pragma: no cover
