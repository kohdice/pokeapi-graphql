from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity


class AuthenticationServiceABC(ABC):
    """Abstract base class for authentication services.

    This class defines the interface for authentication services. Concrete implementations should
    inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def login(self, username: str, password: str) -> BaseEntity:
        """Log in a user with the given credentials.

        Args:
            username (str): The username of the user to log in.
            password (str): The password of the user to log in.

        Returns:
            BaseEntity: The token issued to the logged-in user.

        """
        pass  # pragma: no cover

    @abstractmethod
    def refresh(self, token: str) -> BaseEntity:
        """Refresh a user's token.

        Args:
            token (str): The token to refresh.

        Returns:
            BaseEntity: The refreshed token.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create_user(self, username: str, password: str) -> BaseEntity:
        """Create a new user with the given credentials.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            BaseEntity: The token issued to the new user.

        """
        pass  # pragma: no cover
