from injector import Injector

from pokeapi.dependencies.di.application import ApplicationServiceModule
from pokeapi.dependencies.di.config import ConfigModule
from pokeapi.dependencies.di.database import DatabaseModule
from pokeapi.dependencies.di.repository import RepositoryModule


def get_context() -> dict:
    """Provide a custom context object

    Returns:
        dict: A dictionary with the context object

    """
    return {
        "container": Injector(
            [
                ConfigModule(),
                DatabaseModule(),
                RepositoryModule(),
                ApplicationServiceModule(),
            ]
        )
    }
