import datetime
from unittest.mock import MagicMock

import pytest
from injector import Binder, Injector, singleton
from sqlalchemy.orm import Session

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.application.services.authentication_abc import AuthenticationServiceABC
from pokeapi.application.services.pokemon import PokemonService
from pokeapi.application.services.pokemon_abc import PokemonServiceABC
from pokeapi.application.services.pokemon_ability import AbilityService
from pokeapi.application.services.pokemon_ability_abc import AbilityServiceABC
from pokeapi.application.services.pokemon_type import TypeService
from pokeapi.application.services.pokemon_type_abc import TypeServiceABC
from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.dependencies.settings.config_abc import AppConfigABC
from pokeapi.domain.entities.pokemon import Pokemon
from pokeapi.domain.entities.pokemon_ability import PokemonAbility
from pokeapi.domain.entities.pokemon_stats import PokemonStats
from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.domain.entities.pokemons_ability import PokemonsAbility
from pokeapi.domain.entities.pokemons_type import PokemonsType
from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.token_whitelist import TokenWhitelist
from pokeapi.domain.entities.user import User
from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.domain.repositories.pokemon_ability import AbilityRepositoryABC
from pokeapi.domain.repositories.pokemon_type import TypeRepositoryABC
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.domain.services.jwt import JWTService
from pokeapi.domain.services.jwt_abc import JWTServiceABC
from pokeapi.domain.services.password import PasswordService
from pokeapi.domain.services.password_abc import PasswordServiceABC
from pokeapi.domain.services.token import TokenService
from pokeapi.domain.services.token_abc import TokenServiceABC
from pokeapi.infrastructure.database.db import session_factory
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository
from pokeapi.infrastructure.database.repositories.pokemon_ability import (
    AbilityRepository,
)
from pokeapi.infrastructure.database.repositories.pokemon_type import TypeRepository
from pokeapi.infrastructure.database.repositories.token_whitelist import (
    TokenWhitelistRepository,
)
from pokeapi.infrastructure.database.repositories.user import UserRepository

EXECUTION_DATETIME = datetime.datetime(2000, 1, 1, 0, 10, 0)
ISSUE_DATETIME = datetime.datetime(2000, 1, 1, 0, 0, 0)
TEST_POKEMON_ENTITY = Pokemon(
    id_=1,
    national_pokedex_number=1,
    name="フシギダネ",
    stats=PokemonStats(
        hp=45,
        attack=49,
        defense=49,
        special_attack=65,
        special_defense=65,
        speed=45,
        base_total=318,
    ),
    pokemons_type=(
        PokemonsType(
            pokemon_type=PokemonType(
                id_=5,
                name="くさ",
            ),
            slot=1,
        ),
        PokemonsType(
            pokemon_type=PokemonType(
                id_=8,
                name="どく",
            ),
            slot=2,
        ),
    ),
    pokemons_ability=(
        PokemonsAbility(
            pokemon_ability=PokemonAbility(
                id_=34,
                name="ようりょくそ",
            ),
            slot=3,
            is_hidden=True,
        ),
        PokemonsAbility(
            pokemon_ability=PokemonAbility(
                id_=65,
                name="しんりょく",
            ),
            slot=1,
            is_hidden=False,
        ),
    ),
)
TEST_POKEMON_ABILITY_ENTITY = PokemonAbility(id_=1, name="あくしゅう")
TEST_POKEMON_TYPE_ENTITY = PokemonType(id_=1, name="ノーマル")
TEST_USER_ENTITY = User(id_=1, username="Red", password="hashed_password")
TEST_TOKEN_ENTITY = Token(
    access_token="access_token", refresh_token="refresh_token", token_type="Bearer"
)
TEST_TOKEN_WHITELIST_ENTITY = TokenWhitelist(
    id_=1,
    user_id=1,
    access_token="access_token",
    refresh_token="refresh_token",
    created_by="Red",
    created_at=ISSUE_DATETIME,
    updated_by="Red",
    updated_at=ISSUE_DATETIME,
)


@pytest.fixture(scope="session")
def container() -> Injector:
    def configure(binder: Binder) -> None:
        binder.bind(Session, to=session_factory, scope=singleton)
        binder.bind(AppConfigABC, to=AppConfig, scope=singleton)  # type: ignore

        # Application Services
        binder.bind(
            AuthenticationServiceABC,  # type: ignore
            to=MagicMock(spec=AuthenticationService, autospec=True),
            scope=singleton,
        )
        binder.bind(
            PokemonServiceABC,  # type: ignore
            to=MagicMock(spec=PokemonService, autospec=True),
            scope=singleton,
        )
        binder.bind(
            AbilityServiceABC,  # type: ignore
            to=MagicMock(spec=AbilityService, autospec=True),
            scope=singleton,
        )
        binder.bind(
            TypeServiceABC,  # type: ignore
            to=MagicMock(spec=TypeService, autospec=True),
            scope=singleton,
        )

        # Domain Services
        binder.bind(
            PasswordServiceABC,  # type: ignore
            to=MagicMock(spec=PasswordService, autospec=True),
            scope=singleton,
        )
        binder.bind(
            JWTServiceABC,  # type: ignore
            to=MagicMock(spec=JWTService, autospec=True),
            scope=singleton,
        )
        binder.bind(
            TokenServiceABC,  # type: ignore
            to=MagicMock(spec=TokenService, autospec=True),
            scope=singleton,
        )

        # Repositories
        binder.bind(
            PokemonRepositoryABC,  # type: ignore
            to=MagicMock(spec=PokemonRepository, autospec=True),
            scope=singleton,
        )
        binder.bind(
            AbilityRepositoryABC,  # type: ignore
            to=MagicMock(spec=AbilityRepository, autospec=True),
            scope=singleton,
        )
        binder.bind(
            TypeRepositoryABC,  # type: ignore
            to=MagicMock(spec=TypeRepository, autospec=True),
            scope=singleton,
        )
        binder.bind(
            TokenWhitelistRepositoryABC,  # type: ignore
            to=MagicMock(spec=TokenWhitelistRepository, autospec=True),
            scope=singleton,
        )
        binder.bind(
            UserRepositoryABC,  # type: ignore
            to=MagicMock(spec=UserRepository, autospec=True),
            scope=singleton,
        )

    return Injector(configure)
