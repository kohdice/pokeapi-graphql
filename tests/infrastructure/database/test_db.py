import pytest
from injector import Injector

from pokeapi.dependencies.di.config import ConfigModule
from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.infrastructure.database.db import session_factory
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon


@pytest.fixture(scope="module")
def dependency_container() -> Injector:
    return Injector([ConfigModule()])


def test_session_factory(dependency_container: Injector) -> None:
    session = session_factory(dependency_container.get(AppConfig))
    actual = session.get(Pokemon, 1)

    assert actual is not None
    assert actual.name == "フシギダネ"
