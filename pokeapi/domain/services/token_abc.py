from abc import ABC, abstractmethod

from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.user import User


class TokenServiceABC(ABC):
    """Abstract class for token creation and management.

    This class is an abstract class that defines the methods that a token
    creation and management service should implement.

    """

    @abstractmethod
    def create(self, entity: User) -> Token:
        """Create a token for the given entity.

        Args:
            entity (User): The entity to be used as the payload.

        Returns:
            Token: The token issued to the entity.
        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, entity: User, whitelist_id: int) -> Token:
        """Update a token for the given entity.

        Args:
            entity (User): The entity to be used as the payload.
            whitelist_id (int): The ID of the token to be updated.

        Returns:
            Token: The token issued to the entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, entity: User) -> None:
        """Delete a token for the given entity.

        Args:
            entity (User): The entity to be used as the payload.

        """
        pass  # pragma: no cover
