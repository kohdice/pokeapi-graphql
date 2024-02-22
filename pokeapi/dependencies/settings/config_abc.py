from abc import ABC, abstractmethod


class AppConfigABC(ABC):
    """Abstract base class for app configuration.

    This class defines the interface for application configuration.
    It is used to define the configuration settings for the application.

    Attributes:
        stage: The stage of the application (e.g. 'development', 'staging', 'production').
        debug: A boolean indicating whether the application is in debug mode.
        database_url: The URL for the database connection.

    """

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
