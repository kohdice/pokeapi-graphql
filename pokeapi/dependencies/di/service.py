from injector import Binder, Module, singleton

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.application.services.pokemon_abc import PokemonServiceABC


class ServiceModule(Module):
    """A module for providing service-related dependencies.

    This module provides the service as a dependency to be used by other classes in the application.

    """

    def configure(self, binder: Binder) -> None:
        """Configure the module.

        Args:
            binder (Binder): The binder to configure.

        """
        binder.bind(PokemonServiceABC, to=PokemonService, scope=singleton)  # type: ignore[type-abstract]