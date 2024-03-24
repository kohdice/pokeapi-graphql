import pytest
from injector import Injector
from pytest_mock import MockerFixture
from sqlalchemy import ScalarResult

from pokeapi.infrastructure.database.models.ability_mst import AbilityMst
from pokeapi.infrastructure.database.models.pokemon_abilities import PokemonAbilities
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon
from pokeapi.infrastructure.database.models.pokemon_types import PokemonTypes
from pokeapi.infrastructure.database.models.type_mst import TypeMst
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepository
from tests.conftest import TEST_POKEMON_ENTITY

TEST_MODEL = Pokemon(
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


@pytest.fixture(scope="module")
def repo(container: Injector) -> PokemonRepository:
    return container.get(PokemonRepository)


class TestPokemonRepository:
    def test_convert_to_entity(self, repo: PokemonRepository) -> None:
        assert repo._convert_to_entity(TEST_MODEL) == TEST_POKEMON_ENTITY

    def test_get_by_id(self, repo: PokemonRepository) -> None:
        assert repo.get_by_id(1) == TEST_POKEMON_ENTITY

    def test_get_by_id_not_found(self, repo: PokemonRepository) -> None:
        assert repo.get_by_id(0) is None

    def test_get_by_pokedex_number(self, repo: PokemonRepository) -> None:
        assert repo.get_by_pokedex_number(1) == TEST_POKEMON_ENTITY

    def test_get_by_pokedex_number_not_found(self, repo: PokemonRepository) -> None:
        assert repo.get_by_pokedex_number(0) is None

    def test_get_all(self, repo: PokemonRepository) -> None:
        actual = repo.get_all()

        assert actual
        assert len(actual) == 151
        assert actual[0] == TEST_POKEMON_ENTITY

    def test_get_all_empty(
        self, repo: PokemonRepository, mocker: MockerFixture
    ) -> None:
        mocker.patch.object(ScalarResult, "all", return_value=[])

        assert repo.get_all() == []
