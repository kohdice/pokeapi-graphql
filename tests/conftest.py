import datetime

import pytest
from injector import Binder, Injector, singleton

from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.dependencies.settings.config_abc import AppConfigABC
from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.domain.services.password_abc import PasswordServiceABC
from pokeapi.domain.services.token_abc import TokenServiceABC

from .mocks.domain.password import MockPasswordService
from .mocks.domain.token import MockTokenService
from .mocks.repositories.pokemon import MockPokemonRepository
from .mocks.repositories.token_whitelist import MockTokenWhitelistRepository
from .mocks.repositories.user import MockUserRepository

ISSUE_DATETIME = datetime.datetime(2000, 1, 1, 0, 0, 0)
EXECUTION_DATETIME = datetime.datetime(2000, 1, 1, 0, 10, 0)


@pytest.fixture(scope="session")
def container() -> Injector:
    def configure(binder: Binder) -> None:
        binder.bind(AppConfigABC, to=AppConfig, scope=singleton)  # type: ignore
        binder.bind(PokemonRepositoryABC, to=MockPokemonRepository, scope=singleton)  # type: ignore
        binder.bind(
            TokenWhitelistRepositoryABC,  # type: ignore
            to=MockTokenWhitelistRepository,
            scope=singleton,
        )
        binder.bind(UserRepositoryABC, to=MockUserRepository, scope=singleton)  # type: ignore
        binder.bind(PasswordServiceABC, to=MockPasswordService, scope=singleton)  # type: ignore
        binder.bind(TokenServiceABC, to=MockTokenService, scope=singleton)  # type: ignore

    return Injector(configure)
