from injector import inject, provider, singleton
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.infrastructure.database.utils import adjust_connection_url


@singleton
@inject
@provider
def session_factory(config: AppConfig) -> Session:
    """Create a new session factory.

    Args:
        config (AppConfig): The application configuration.

    Returns:
        Session: A new session factory.

    """
    engine = create_engine(
        adjust_connection_url(config.database_url), echo=config.debug
    )
    session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    with session_local() as session:
        return session
