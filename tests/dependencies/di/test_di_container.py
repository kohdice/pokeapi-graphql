import pytest
from injector import Injector
from sqlalchemy import select
from sqlalchemy.orm import Session

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.dependencies.di.config import ConfigModule
from pokeapi.dependencies.di.database import DatabaseModule
from pokeapi.dependencies.di.repository import RepositoryModule
from pokeapi.dependencies.di.service import ServiceModule
from pokeapi.dependencies.settings import AppConfig
from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.infrastructure.database.models import Pokemon as PokemonModel
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository


class TestDIContainer:
    @pytest.fixture(scope="module")
    def dependency_container(self) -> Injector:
        return Injector(
            [ConfigModule(), DatabaseModule(), RepositoryModule(), ServiceModule()]
        )

    def test_singleton(self, dependency_container: Injector) -> None:
        session_1 = dependency_container.get(Session)
        session_2 = dependency_container.get(Session)

        assert session_1 is session_2

        config_1 = dependency_container.get(AppConfig)
        config_2 = dependency_container.get(AppConfig)

        assert config_1 is config_2

        repo_1 = dependency_container.get(PokemonRepository)
        repo_2 = dependency_container.get(PokemonRepository)

        assert repo_1 is repo_2

        service_1 = dependency_container.get(PokemonService)
        service_2 = dependency_container.get(PokemonService)

        assert service_1 is service_2

    def test_di_config(self, dependency_container: Injector) -> None:
        actual = dependency_container.get(AppConfig)

        assert actual.stage == "development"

    def test_di_db(self, dependency_container: Injector) -> None:
        session = dependency_container.get(Session)

        actual = session.execute(
            select(PokemonModel).where(PokemonModel.id_ == 1)
        ).scalar()

        assert isinstance(actual, PokemonModel)
        assert actual.name == "フシギダネ"

    def test_di_pokemon_repo(self, dependency_container: Injector) -> None:
        repo = dependency_container.get(PokemonRepository)
        actual_1 = repo.get_by_id(1)

        assert isinstance(actual_1, PokemonEntity)
        assert actual_1.name == "フシギダネ"

    def test_di_pokemon_service(self, dependency_container: Injector) -> None:
        service = dependency_container.get(PokemonService)
        actual_1 = service.get_by_id(1)

        assert isinstance(actual_1, PokemonEntity)
        assert actual_1.name == "フシギダネ"
