from injector import inject, singleton

from pokeapi.domain.entities.pokemon import Pokemon
from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC

from .pokemon_abc import PokemonServiceABC


@singleton
class PokemonService(PokemonServiceABC):
    """Concrete implementation of a Pokémon service.

    This class provides concrete implementations of the abstract methods defined in the
    PokemonServiceABC class. It is responsible for retrieving Pokémon from the repository.

    Attributes:
        _repo (PokemonRepositoryABC): The repository used by the service.

    """

    @inject
    def __init__(self, repo: PokemonRepositoryABC):
        """Initialize the PokemonService with a repository.

        Args:
            repo (PokemonRepositoryABC): The repository used by the service.

        """
        self._repo = repo

    def get_by_id(self, id_: int) -> Pokemon | None:
        """Retrieve a pokemon by its identifier.

        Args:
            id_ (int): The identifier of the Pokémon to retrieve.

        Returns:
            Pokemon | None: The Pokémon with the given identifier, or None if it does not exist.

        """
        return self._repo.get_by_id(id_)

    def get_by_pokedex_number(self, pokedex_number: int) -> Pokemon | None:
        """Retrieve a Pokémon by its Pokédex number.

        Args:
            pokedex_number (int): The Pokédex number of the Pokémon to retrieve.

        Returns:
            Pokemon | None: The Pokémon with the specified Pokédex number, or None if not found.

        """
        return self._repo.get_by_pokedex_number(pokedex_number)

    def get_by_name(self, name: str) -> Pokemon | None:
        """Retrieve a Pokémon by its name.

        Args:
            name (str): The name of the Pokémon to retrieve.

        Returns:
            Pokemon | None: The Pokémon with the specified name, or None if not found.

        """
        return self._repo.get_by_name(name)

    def get_all(self) -> list[Pokemon]:
        """Retrieve all Pokémon from the repository.

        Returns:
            list[Pokemon]: A list of all Pokémon in the repository.

        """
        return self._repo.get_all()
