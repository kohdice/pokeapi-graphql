from injector import inject, singleton

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.repositories.pokemon_type import TypeRepositoryABC

from .pokemon_type_abc import TypeServiceABC


@singleton
class TypeService(TypeServiceABC):
    """Concrete implementation of a type service.

    This class provides concrete implementations of the abstract methods defined in the
    TypeServiceABC class. It is responsible for retrieving types from the repository.

    Attributes:
        _repo (TypeRepositoryABC): The repository used by the service.

    """

    @inject
    def __init__(self, repo: TypeRepositoryABC):
        """Initialize the TypeService with a repository.

        Args:
            repo (TypeRepositoryABC): The repository used by the service.

        """
        self._repo = repo

    def get_by_id(self, id_: int) -> BaseEntity | None:
        """Retrieve a type by its identifier.

        Args:
            id_ (int): The identifier of the type to retrieve.

        Returns:
            BaseEntity | None: The type with the specified identifier, or None if not found.

        """
        return self._repo.get_by_id(id_)

    def get_all(self) -> list[BaseEntity]:
        """Retrieve all type from the repository.

        Returns:
            list[BaseEntity]: A list of all type in the repository.

        """
        return self._repo.get_all()
