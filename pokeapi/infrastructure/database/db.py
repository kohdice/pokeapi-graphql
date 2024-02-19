from typing import NewType

from injector import provider, singleton
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pokeapi.infrastructure.database.utils import adjust_connection_url

ConnectionUrl = NewType("ConnectionUrl", str)


@singleton
@provider
def session_factory(connection_url: ConnectionUrl) -> sessionmaker[Session]:
    """Create a new session factory.

    Args:
        connection_url (ConnectionUrl): The connection URL.

    Returns:
        sessionmaker: The session factory.

    """
    engine = create_engine(adjust_connection_url(connection_url), echo=True)

    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
