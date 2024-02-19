import os

import pytest
from pytest_mock import MockFixture
from sqlalchemy import ScalarResult

from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.domain.entities.pokemon_ability import PokemonAbility
from pokeapi.domain.entities.pokemon_stats import PokemonStats
from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.domain.entities.pokemons_ability import PokemonsAbility
from pokeapi.domain.entities.pokemons_type import PokemonsType
from pokeapi.infrastructure.database.db import ConnectionUrl, session_factory
from pokeapi.infrastructure.database.models.ability_mst import AbilityMst
from pokeapi.infrastructure.database.models.pokemon_abilities import PokemonAbilities
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon as PokemonModel
from pokeapi.infrastructure.database.models.pokemon_types import PokemonTypes
from pokeapi.infrastructure.database.models.type_mst import TypeMst
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository

TEST_MODEL = PokemonModel(
    id_=1,
    national_pokedex_number=1,
    name="フシギダネ",
    hp=45,
    attack=49,
    defense=49,
    special_attack=65,
    special_defense=65,
    speed=45,
    base_total=318,
    pokemon_types=[
        PokemonTypes(
            type_=TypeMst(
                id_=5,
                type_="くさ",
            ),
            slot=1,
        ),
        PokemonTypes(
            type_=TypeMst(
                id_=8,
                type_="どく",
            ),
            slot=2,
        ),
    ],
    pokemon_abilities=[
        PokemonAbilities(
            ability=AbilityMst(
                id_=34,
                ability="ようりょくそ",
            ),
            slot=3,
            is_hidden=True,
        ),
        PokemonAbilities(
            ability=AbilityMst(
                id_=65,
                ability="しんりょく",
            ),
            slot=1,
            is_hidden=False,
        ),
    ],
)

TEST_ENTITY = PokemonEntity(
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


class TestPokemonRepository:
    CONNECTION_URL = ConnectionUrl(os.environ["DATABASE_URL"])

    @pytest.mark.parametrize(("model", "expected"), [(TEST_MODEL, TEST_ENTITY)])
    def test_convert_to_entity(
        self, model: PokemonModel, expected: PokemonEntity
    ) -> None:
        session = session_factory(self.CONNECTION_URL)
        with session() as s:
            repo = PokemonRepository(s)
            actual = repo._convert_to_entity(model)

            assert actual == expected

    @pytest.mark.parametrize("expected", [TEST_ENTITY])
    def test_get_by_id(self, expected: PokemonEntity) -> None:
        session = session_factory(self.CONNECTION_URL)
        with session() as s:
            repo = PokemonRepository(s)
            actual = repo.get_by_id(1)

            assert actual == expected

    def test_get_by_id_not_found(self) -> None:
        session = session_factory(self.CONNECTION_URL)
        with session() as s:
            repo = PokemonRepository(s)
            actual = repo.get_by_id(0)

            assert actual is None

    @pytest.mark.parametrize("expected", [TEST_ENTITY])
    def test_get_all(self, expected: PokemonEntity) -> None:
        session = session_factory(self.CONNECTION_URL)
        with session() as s:
            repo = PokemonRepository(s)
            actual = repo.get_all()

            assert actual
            assert len(actual) == 151
            assert actual[0] == expected

    def test_get_all_empty(self, mocker: MockFixture) -> None:
        mocker.patch.object(ScalarResult, "all", return_value=[])
        session = session_factory(self.CONNECTION_URL)
        with session() as s:
            repo = PokemonRepository(s)
            actual = repo.get_all()

            assert actual == []
