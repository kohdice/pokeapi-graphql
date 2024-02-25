import pytest
from injector import Injector
from pytest_mock import MockerFixture
from sqlalchemy import ScalarResult
from sqlalchemy.orm import Session

from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.infrastructure.database.models.type_mst import TypeMst
from pokeapi.infrastructure.database.repositories.pokemon_type import TypeRepository

TEST_MODEL = TypeMst(
    id_=1,
    type_="ノーマル",
)

TEST_ENTITY = PokemonType(id_=1, name="ノーマル")


@pytest.fixture(scope="module")
def repo(dependency_container: Injector) -> TypeRepository:
    session = dependency_container.get(Session)

    return TypeRepository(session)


class TestTypeRepository:
    def test_convert_to_entity(self, repo: TypeRepository) -> None:
        assert repo._convert_to_entity(TEST_MODEL) == TEST_ENTITY

    def test_get_by_id(self, repo: TypeRepository) -> None:
        assert repo.get_by_id(1) == TEST_ENTITY

    def test_get_by_id_not_found(self, repo: TypeRepository) -> None:
        assert repo.get_by_id(0) is None

    def test_get_all(self, repo: TypeRepository) -> None:
        actual = repo.get_all()

        assert actual
        assert len(actual) == 18
        assert actual[0] == TEST_ENTITY

    def test_get_all_empty(self, repo: TypeRepository, mocker: MockerFixture) -> None:
        mocker.patch.object(ScalarResult, "all", return_value=[])

        assert repo.get_all() == []
