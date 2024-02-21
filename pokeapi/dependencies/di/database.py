from injector import Module, provider, singleton
from sqlalchemy.orm import Session

from pokeapi.dependencies.settings import AppConfig
from pokeapi.infrastructure.database.db import session_factory


class DatabaseModule(Module):
    """A module for providing database-related dependencies.

    This module provides the database session and connection URL as dependencies
    to be used by other classes in the application.

    """

    @singleton
    @provider
    def provide_db_session(self, config: AppConfig) -> Session:
        """Provides the database session for the application.

            This method provides the database session for the application as a dependency.

        Args:
            config (AppConfig): The application configuration.

        Returns:
            Session: The database session for the application.

        """
        session_local = session_factory(config)
        session = session_local()

        try:
            return session
        finally:
            session.close()
