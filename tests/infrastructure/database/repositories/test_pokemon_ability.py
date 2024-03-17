import pytest
from injector import Injector
from pytest_mock import MockerFixture
from sqlalchemy import ScalarResult

from pokeapi.infrastructure.database.models.ability_mst import AbilityMst
from pokeapi.infrastructure.database.repositories.pokemon_ability import (
    AbilityRepository,
)
from tests.conftest import TEST_POKEMON_ABILITY_ENTITY

TEST_MODEL = AbilityMst(id_=1, ability="あくしゅう")


@pytest.fixture(scope="module")
def repo(container: Injector) -> AbilityRepository:
    return container.get(AbilityRepository)


class TestAbilityRepository:
    def test_convert_to_entity(self, repo: AbilityRepository) -> None:
        assert repo._convert_to_entity(TEST_MODEL) == TEST_POKEMON_ABILITY_ENTITY

    def test_get_by_id(self, repo: AbilityRepository) -> None:
        assert repo.get_by_id(1) == TEST_POKEMON_ABILITY_ENTITY

    def test_get_by_id_not_found(self, repo: AbilityRepository) -> None:
        assert repo.get_by_id(0) is None

    def test_get_all(self, repo: AbilityRepository) -> None:
        actual = repo.get_all()

        assert actual
        assert len(actual) == 302
        assert actual[0] == TEST_POKEMON_ABILITY_ENTITY

    def test_get_all_empty(
        self, repo: AbilityRepository, mocker: MockerFixture
    ) -> None:
        mocker.patch.object(ScalarResult, "all", return_value=[])

        assert repo.get_all() == []
