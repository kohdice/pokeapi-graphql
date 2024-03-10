from injector import Binder, Module, singleton

from pokeapi.domain.services.password import PasswordService
from pokeapi.domain.services.password_abc import PasswordServiceABC
from pokeapi.domain.services.token import TokenService
from pokeapi.domain.services.token_abc import TokenServiceABC


class DomainServiceModule(Module):
    """A module for providing domain service-related dependencies.

    This module provides the domain service as a dependency to be used by other classes in the domain.

    """

    def configure(self, binder: Binder) -> None:
        """Configure the module.

        Args:
            binder (Binder): The binder to configure.

        """
        binder.bind(PasswordServiceABC, to=PasswordService, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(TokenServiceABC, to=TokenService, scope=singleton)  # type: ignore[type-abstract]
