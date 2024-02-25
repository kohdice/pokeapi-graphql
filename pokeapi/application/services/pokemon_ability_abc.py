from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity


class AbilityServiceABC(ABC):
    """Abstract base class for ability services.

    This class defines the interface for ability services. Concrete implementations should
    inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def get_by_id(self, id_: int) -> BaseEntity | None:
        """Retrieve a type by its identifier.

        Args:
            id_ (int): The identifier of the ability to retrieve.

        Returns:
            BaseEntity | None: The ability with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[BaseEntity]:
        """Retrieve all ability from the repository.

        Returns:
            list[BaseEntity]: A list of all ability in the repository.

        """
        pass  # pragma: no cover
