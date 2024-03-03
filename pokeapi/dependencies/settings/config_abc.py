from abc import ABC, abstractmethod
from functools import cache


class AppConfigABC(ABC):
    """Abstract base class for app configuration.

    This class defines the interface for application configuration.
    It is used to define the configuration settings for the application.

    Attributes:
        stage: The stage of the application (e.g. 'development', 'staging', 'production').
        debug: A boolean indicating whether the application is in debug mode.
        database_url: The URL for the database connection.
        private_key: The private key for the application.
        public_key: The public key for the application.
        jwt_algorithm: The algorithm to use for JWT signing.
        access_token_lifetime: The lifetime of access tokens (in hours).
        refresh_token_lifetime: The lifetime of refresh tokens (in hours).

    """

    @staticmethod
    @cache
    @abstractmethod
    def _load_private_key() -> bytes:
        """Load the private key for the application.

        Returns:
            bytes: The private key for the application.

        """
        pass  # pragma: no cover

    @staticmethod
    @cache
    @abstractmethod
    def _load_public_key() -> bytes:
        """Load the public key for the application.

        Returns:
            bytes: The public key for the application.

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
    def private_key(self) -> bytes:
        """The private key for the application.

        Returns:
            bytes: The private key for the application.

        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def public_key(self) -> bytes:
        """The public key for the application.

        Returns:
            bytes: The public key for the application.

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
