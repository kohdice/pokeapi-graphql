import os

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

    @property
    def stage(self) -> str:
        """The stage of the application (e.g. 'development', 'staging', 'production').

        Returns:
            str: The stage of the application.

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

        """
        url = os.getenv("DATABASE_URL")

        if url is None:
            raise UnsetEnvironmentVariableError(
                "DATABASE_URL environment variable is not set"
            )

        return url
