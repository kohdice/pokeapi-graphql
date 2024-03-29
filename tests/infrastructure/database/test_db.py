from injector import Injector

from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.infrastructure.database.db import session_factory
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon


def test_session_factory(container: Injector) -> None:
    session = session_factory(container.get(AppConfig))
    actual = session.get(Pokemon, 1)

    assert actual is not None
    assert actual.name == "フシギダネ"
