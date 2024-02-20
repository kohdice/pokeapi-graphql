from abc import ABC, abstractmethod
from typing import NewType

ConnectionUrl = NewType("ConnectionUrl", str)


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
        pass

    @property
    @abstractmethod
    def debug(self) -> bool:
        """A boolean indicating whether the application is in debug mode.

        Returns:
            bool: A boolean indicating whether the application is in debug mode.

        """
        pass

    @property
    @abstractmethod
    def database_url(self) -> ConnectionUrl:
        """The URL for the database connection.

        Returns:
            ConnectionUrl: The URL for the database connection.

        """
        pass
