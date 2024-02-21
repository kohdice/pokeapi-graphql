from injector import provider, singleton
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pokeapi.dependencies.settings import AppConfig
from pokeapi.infrastructure.database.utils import adjust_connection_url


@singleton
@provider
def session_factory(config: AppConfig) -> sessionmaker[Session]:
    """Create a new session factory.

    Args:
        config (AppConfig): The application configuration.

    Returns:
        sessionmaker: The session factory.

    """
    engine = create_engine(
        adjust_connection_url(config.database_url), echo=config.debug
    )

    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
