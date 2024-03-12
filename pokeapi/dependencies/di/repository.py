from injector import Binder, Module, singleton

from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.domain.repositories.pokemon_ability import AbilityRepositoryABC
from pokeapi.domain.repositories.pokemon_type import TypeRepositoryABC
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository
from pokeapi.infrastructure.database.repositories.pokemon_ability import (
    AbilityRepository,
)
from pokeapi.infrastructure.database.repositories.pokemon_type import TypeRepository
from pokeapi.infrastructure.database.repositories.token_whitelist import (
    TokenWhitelistRepository,
)
from pokeapi.infrastructure.database.repositories.user import UserRepository


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
        binder.bind(AbilityRepositoryABC, to=AbilityRepository, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(
            TokenWhitelistRepositoryABC,  # type: ignore[type-abstract]
            to=TokenWhitelistRepository,
            scope=singleton,
        )
        binder.bind(TypeRepositoryABC, to=TypeRepository, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(UserRepositoryABC, to=UserRepository, scope=singleton)  # type: ignore[type-abstract]
