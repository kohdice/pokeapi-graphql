from injector import Binder, Module, singleton

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.application.services.authentication_abc import AuthenticationServiceABC
from pokeapi.application.services.pokemon import PokemonService
from pokeapi.application.services.pokemon_abc import PokemonServiceABC
from pokeapi.application.services.pokemon_ability import AbilityService
from pokeapi.application.services.pokemon_ability_abc import AbilityServiceABC
from pokeapi.application.services.pokemon_type import TypeService
from pokeapi.application.services.pokemon_type_abc import TypeServiceABC


class ApplicationServiceModule(Module):
    """A module for providing application service-related dependencies.

    This module provides the application service as a dependency
    to be used by other classes in the application.

    """

    def configure(self, binder: Binder) -> None:
        """Configure the module.

        Args:
            binder (Binder): The binder to configure.

        """
        binder.bind(AuthenticationServiceABC, to=AuthenticationService, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(AbilityServiceABC, to=AbilityService, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(PokemonServiceABC, to=PokemonService, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(TypeServiceABC, to=TypeService, scope=singleton)  # type: ignore[type-abstract]
