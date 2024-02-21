import pytest
from injector import Injector
from sqlalchemy import select
from sqlalchemy.orm import Session

from pokeapi.dependencies.di.config import ConfigModule
from pokeapi.dependencies.di.database import DatabaseModule
from pokeapi.dependencies.di.repository import RepositoryModule
from pokeapi.dependencies.settings import AppConfig
from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.infrastructure.database.models import Pokemon as PokemonModel
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository


class TestDIContainer:
    @pytest.fixture()
    def di(self) -> Injector:
        return Injector([ConfigModule(), DatabaseModule(), RepositoryModule()])

    def test_singleton(self, di: Injector) -> None:
        session_1 = di.get(Session)
        session_2 = di.get(Session)

        assert session_1 is session_2

        config_1 = di.get(AppConfig)
        config_2 = di.get(AppConfig)

        assert config_1 is config_2

        repo_1 = di.get(PokemonRepository)
        repo_2 = di.get(PokemonRepository)

        assert repo_1 is repo_2

    def test_di_config(self, di: Injector) -> None:
        actual = di.get(AppConfig)

        assert actual.stage == "development"

    def test_di_db(self, di: Injector) -> None:
        session = di.get(Session)

        actual = session.execute(
            select(PokemonModel).where(PokemonModel.id_ == 1)
        ).scalar()

        assert isinstance(actual, PokemonModel)
        assert actual.name == "フシギダネ"

    def test_di_pokemon_repo(self, di: Injector) -> None:
        repo = di.get(PokemonRepository)
        actual_1 = repo.get_by_id(1)

        assert isinstance(actual_1, PokemonEntity)
        assert actual_1.name == "フシギダネ"
