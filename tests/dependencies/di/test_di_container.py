import pytest
from injector import Injector
from sqlalchemy import select
from sqlalchemy.orm import Session

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.dependencies.di.application import ApplicationServiceModule
from pokeapi.dependencies.di.config import ConfigModule
from pokeapi.dependencies.di.database import DatabaseModule
from pokeapi.dependencies.di.domain import DomainServiceModule
from pokeapi.dependencies.di.repository import RepositoryModule
from pokeapi.dependencies.settings import AppConfig
from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.domain.services.password import PasswordService
from pokeapi.infrastructure.database.models import Pokemon as PokemonModel
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository


class TestDIContainer:
    @pytest.fixture(scope="module")
    def dependency_container(self) -> Injector:
        return Injector(
            [
                ConfigModule(),
                DatabaseModule(),
                DomainServiceModule(),
                RepositoryModule(),
                ApplicationServiceModule(),
            ]
        )

    def test_singleton(self, dependency_container: Injector) -> None:
        session_1 = dependency_container.get(Session)
        session_2 = dependency_container.get(Session)

        assert isinstance(session_1, Session)
        assert session_1 is session_2

        config_1 = dependency_container.get(AppConfig)
        config_2 = dependency_container.get(AppConfig)

        assert isinstance(config_1, AppConfig)
        assert config_1 is config_2

        repo_1 = dependency_container.get(PokemonRepository)
        repo_2 = dependency_container.get(PokemonRepository)

        assert isinstance(repo_1, PokemonRepository)
        assert repo_1 is repo_2

        app_service_1 = dependency_container.get(PokemonService)
        app_service_2 = dependency_container.get(PokemonService)

        assert isinstance(app_service_1, PokemonService)
        assert app_service_1 is app_service_2

        domain_service_1 = dependency_container.get(PasswordService)
        domain_service_2 = dependency_container.get(PasswordService)

        assert isinstance(domain_service_1, PasswordService)
        assert domain_service_1 is domain_service_2

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
        actual = repo.get_by_id(1)

        assert isinstance(actual, PokemonEntity)
        assert actual.name == "フシギダネ"

    def test_di_pokemon_service(self, dependency_container: Injector) -> None:
        service = dependency_container.get(PokemonService)
        actual = service.get_by_id(1)

        assert isinstance(actual, PokemonEntity)
        assert actual.name == "フシギダネ"

    def test_di_password_service(self, dependency_container: Injector) -> None:
        service = dependency_container.get(PasswordService)
        actual = service.hash("password")

        assert isinstance(actual, str)
