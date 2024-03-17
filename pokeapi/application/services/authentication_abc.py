from abc import ABC, abstractmethod

from pokeapi.domain.entities.token import Token


class AuthenticationServiceABC(ABC):
    """Abstract base class for authentication services.

    This class defines the interface for authentication services. Concrete implementations should
    inherit from this class and provide implementations for the abstract methods.

    """

    @abstractmethod
    def auth(self, username: str, password: str) -> Token:
        """Authenticate a user with the given credentials.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            Token: The token issued to the user.

        """
        pass  # pragma: no cover

    @abstractmethod
    def refresh(self, token: str) -> Token:
        """Refresh a user's token.

        Args:
            token (str): The token to refresh.

        Returns:
            Token: The refreshed token.

        """
        pass  # pragma: no cover
