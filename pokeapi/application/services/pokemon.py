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

    def get_all(self) -> list[Pokemon]:
        """Retrieve all Pokémon from the repository.

        Returns:
            list[Pokemon]: A list of all Pokémon in the repository.

        """
        return self._repo.get_all()
