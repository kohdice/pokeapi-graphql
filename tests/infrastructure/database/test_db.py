import os

from pokeapi.infrastructure.database.db import ConnectionUrl, session_factory
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon


def test_session_factory() -> None:
    url = ConnectionUrl(os.environ["DATABASE_URL"])
    session = session_factory(url)

    with session() as s:
        actual = s.get(Pokemon, 1)

        assert actual is not None
        assert actual.name == "フシギダネ"
