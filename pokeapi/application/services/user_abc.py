from abc import ABC, abstractmethod

from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.user import User


class UserServiceABC(ABC):
    """Abstract base class for user services.

    This class defines the interface for user services. Concrete implementations should inherit from
    this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def get_by_token(self, token: str) -> User:
        """Get the user associated with the given token.

        Args:
            token (str): The token to use for retrieval.

        Returns:
            User: The user with the given ID.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, username: str, password: str) -> Token:
        """Create a new user with the given credentials.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            Token: The token issued to the new user.

        """
        pass  # pragma: no cover
