from injector import Binder, Module, singleton
from sqlalchemy.orm import Session

from pokeapi.infrastructure.database.db import session_factory


class DatabaseModule(Module):
    """A module for providing database-related dependencies.

    This module provides the database session and connection URL as dependencies
    to be used by other classes in the application.

    """

    def configure(self, binder: Binder) -> None:
        """Configure the database module.

        Args:
            binder (Binder): The binder to configure.

        """

        binder.bind(Session, to=session_factory, scope=singleton)
