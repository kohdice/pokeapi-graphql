import pytest
from injector import Injector
from pytest_mock import MockerFixture

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.domain.entities.base import BaseEntity

from .conftest import MockPokemonRepository


@pytest.fixture()
def service(dependency_container: Injector) -> PokemonService:
    repo = dependency_container.get(MockPokemonRepository)

    return PokemonService(repo)


class TestPokemonService:
    @pytest.mark.parametrize("id_", [1, 2])
    def test_get_by_id(self, service: PokemonService, id_: int) -> None:
        actual = service.get_by_id(id_)

        assert isinstance(actual, BaseEntity)

    def test_get_by_id_not_found(self, service: PokemonService) -> None:
        actual = service.get_by_id(0)

        assert actual is None

    def test_get_all(self, service: PokemonService) -> None:
        actual = service.get_all()

        assert len(actual) == 2
        assert isinstance(actual[0], BaseEntity)
        assert isinstance(actual[1], BaseEntity)

    def test_get_all_empty(
        self, service: PokemonService, mocker: MockerFixture
    ) -> None:
        mocker.patch.object(service._repo, "get_all", return_value=[])

        actual = service.get_all()

        assert actual == []
