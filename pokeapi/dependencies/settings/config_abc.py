from abc import ABC, abstractmethod
from functools import cache


class AppConfigABC(ABC):
    """Abstract base class for app configuration.

    This class defines the interface for application configuration.
    It is used to define the configuration settings for the application.

    """

    @staticmethod
    @cache
    @abstractmethod
    def _load_private_key() -> str:
        """Load the private key for the application.

        Returns:
            str: The private key for the application.

        """
        pass  # pragma: no cover

    @staticmethod
    @cache
    @abstractmethod
    def _load_public_key() -> str:
        """Load the public key for the application.

        Returns:
            str: The public key for the application.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def stage(self) -> str:
        """The stage of the application (e.g. 'development', 'staging', 'production').

        Returns:
            str: The stage of the application.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def debug(self) -> bool:
        """A boolean indicating whether the application is in debug mode.

        Returns:
            bool: A boolean indicating whether the application is in debug mode.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def database_url(self) -> str:
        """The URL for the database connection.

        Returns:
            str: The URL for the database connection.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def private_key(self) -> str:
        """The private key for the application.

        Returns:
            str: The private key for the application.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def public_key(self) -> str:
        """The public key for the application.

        Returns:
            str: The public key for the application.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def jwt_algorithm(self) -> str:
        """The algorithm to use for JWT signing.

        Returns:
            str: The algorithm to use for JWT signing.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def access_token_lifetime(self) -> int:
        """The lifetime of access tokens (in hours).

        Returns:
            int: The lifetime of access tokens.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def refresh_token_lifetime(self) -> int:
        """The lifetime of refresh tokens (in hours).

        Returns:
            int: The lifetime of refresh tokens.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def app_domain(self) -> str:
        """The domain of the application.

        Returns:
            str: The domain of the application.

        """
        pass  # pragma: no cover
