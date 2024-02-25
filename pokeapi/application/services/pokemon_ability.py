from injector import inject, singleton

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.repositories.pokemon_ability import AbilityRepositoryABC

from .pokemon_ability_abc import AbilityServiceABC


@singleton
class AbilityService(AbilityServiceABC):
    """Concrete implementation of a ability service.

    This class provides concrete implementations of the abstract methods defined in the
    AbilityServiceABC class. It is responsible for retrieving abilities from the repository.

    Attributes:
        _repo (AbilityRepositoryABC): The repository used by the service.

    """

    @inject
    def __init__(self, repo: AbilityRepositoryABC):
        """Initialize the AbilityService with a repository.

        Args:
            repo (AbilityRepositoryABC): The repository used by the service.

        """
        self._repo = repo

    def get_by_id(self, id_: int) -> BaseEntity | None:
        """Retrieve a ability by its identifier.

        Args:
            id_ (int): The identifier of the ability to retrieve.

        Returns:
            BaseEntity | None: The ability with the specified identifier, or None if not found.

        """
        return self._repo.get_by_id(id_)

    def get_all(self) -> list[BaseEntity]:
        """Retrieve all ability from the repository.

        Returns:
            list[BaseEntity]: A list of all ability in the repository.

        """
        return self._repo.get_all()
