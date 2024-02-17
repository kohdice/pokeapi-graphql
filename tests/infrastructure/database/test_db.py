import os

from pokeapi.infrastructure.database.db import session_factory
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon


def test_session_factory():
    session = session_factory(os.environ["DATABASE_URL"])

    with session() as s:
        actual = s.get(Pokemon, 1)

        assert actual is not None
        assert actual.name == "フシギダネ"
