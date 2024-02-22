from injector import Binder, Module, singleton

from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository


class RepositoryModule(Module):
    """A module for providing repository-related dependencies.

    This module provides the repository as a dependency to be used by other classes in the application.

    """

    def configure(self, binder: Binder) -> None:
        """Configure the module.

        Args:
            binder (Binder): The binder to configure.

        """
        binder.bind(PokemonRepositoryABC, to=PokemonRepository, scope=singleton)  # type: ignore[type-abstract]
