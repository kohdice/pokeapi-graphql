from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity


class TypeServiceABC(ABC):
    """Abstract base class for type services.

    This class defines the interface for type services. Concrete implementations should
    inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def get_by_id(self, id_: int) -> BaseEntity | None:
        """Retrieve a type by its identifier.

        Args:
            id_ (int): The identifier of the type to retrieve.

        Returns:
            BaseEntity | None: The type with the specified identifier, or None if not found.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_all(self) -> list[BaseEntity]:
        """Retrieve all type from the repository.

        Returns:
            list[BaseEntity]: A list of all type in the repository.

        """
        pass  # pragma: no cover
