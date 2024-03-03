import os
from functools import cache

from injector import singleton

from pokeapi.exceptions.config import (
    InvalidEnvironmentValueError,
    UnsetEnvironmentVariableError,
)

from .config_abc import AppConfigABC


@singleton
class AppConfig(AppConfigABC):
    """The application configuration.

    This class is responsible for providing the configuration to the application.

    """

    @staticmethod
    @cache
    def _load_private_key() -> bytes:
        """Load the private key from the environment.

        Returns:
            bytes: The private key for the application.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        private_key_path = os.getenv("PRIVATE_KEY")

        if private_key_path is None:
            raise UnsetEnvironmentVariableError(
                "PRIVATE_KEY environment variable is not set"
            )
        with open(private_key_path, "rb") as f:
            return f.read()

    @staticmethod
    @cache
    def _load_public_key() -> bytes:
        """Load the public key from the environment.

        Returns:
            bytes: The public key for the application.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        public_key_path = os.getenv("PUBLIC_KEY")

        if public_key_path is None:
            raise UnsetEnvironmentVariableError(
                "PUBLIC_KEY environment variable is not set"
            )

        with open(public_key_path, "rb") as f:
            return f.read()

    @property
    def stage(self) -> str:
        """The stage of the application (e.g. 'development', 'staging', 'production').

        Returns:
            str: The stage of the application.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.
            InvalidEnvironmentValueError: If the environment variable has an invalid value.

        """
        stage = os.getenv("STAGE")

        if stage is None:
            raise UnsetEnvironmentVariableError("STAGE is unset")

        if stage.lower() not in ("development", "staging", "production"):
            raise InvalidEnvironmentValueError(
                f"Environment variable has an invalid value. STAGE: {stage}"
            )

        return stage.lower()

    @property
    def debug(self) -> bool:
        """A boolean indicating whether the application is in debug mode.

        Returns:
            bool: A boolean indicating whether the application is in debug mode.

        """
        env_value = os.getenv("DEBUG")

        if env_value is not None:
            return env_value.lower() == "true"

        return False

    @property
    def database_url(self) -> str:
        """The URL for the database connection.

        Returns:
            str: The URL for the database connection.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        url = os.getenv("DATABASE_URL")

        if url is None:
            raise UnsetEnvironmentVariableError(
                "DATABASE_URL environment variable is not set"
            )

        return url

    @property
    def private_key(self) -> bytes:
        """The private key for the application.

        Returns:
            bytes: The private key for the application.

        """
        return self._load_private_key()

    @property
    def public_key(self) -> bytes:
        """The public key for the application.

        Returns:
            bytes: The public key for the application.

        """
        return self._load_public_key()

    @property
    def jwt_algorithm(self) -> str:
        """The algorithm to use for JWT signing.

        Returns:
            str: The algorithm to use for JWT signing.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        algorithm = os.getenv("JWT_ALGORITHM")

        if algorithm is None:
            raise UnsetEnvironmentVariableError(
                "JWT_ALGORITHM environment variable is not set"
            )

        return algorithm

    @property
    def access_token_lifetime(self) -> int:
        """The lifetime of access tokens in hours.

        Returns:
            int: The lifetime of access tokens in hours.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        lifetime = os.getenv("ACCESS_TOKEN_LIFETIME")

        if lifetime is None:
            raise UnsetEnvironmentVariableError(
                "ACCESS_TOKEN_LIFETIME environment variable is not set"
            )

        return int(lifetime)

    @property
    def refresh_token_lifetime(self) -> int:
        """The lifetime of refresh tokens in hours.

        Returns:
            int: The lifetime of refresh tokens in hours.

        Reises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        lifetime = os.getenv("REFRESH_TOKEN_LIFETIME")

        if lifetime is None:
            raise UnsetEnvironmentVariableError(
                "REFRESH_TOKEN_LIFETIME environment variable is not set"
            )

        return int(lifetime)

    @property
    def app_domain(self) -> str:
        """The domain of the application.

        Returns:
            str: The domain of the application.

        Raises:
            UnsetEnvironmentVariableError: If the environment variable is not set.

        """
        domain = os.getenv("APP_DOMAIN")

        if domain is None:
            raise UnsetEnvironmentVariableError(
                "APP_DOMAIN environment variable is not set"
            )

        return domain
