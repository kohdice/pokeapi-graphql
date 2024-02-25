import pytest
from injector import Injector
from pytest_mock import MockerFixture

from pokeapi.application.services.pokemon_type import TypeService
from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.repositories.pokemon_type import TypeRepositoryABC


@pytest.fixture()
def service(dependency_container: Injector) -> TypeService:
    repo = dependency_container.get(TypeRepositoryABC)  # type: ignore[type-abstract]

    return TypeService(repo)


class TestTypeService:
    @pytest.mark.parametrize("id_", [1, 2])
    def test_get_by_id(self, service: TypeService, id_: int) -> None:
        actual = service.get_by_id(id_)

        assert isinstance(actual, BaseEntity)

    def test_get_by_id_not_found(self, service: TypeService) -> None:
        assert service.get_by_id(0) is None

    def test_get_all(self, service: TypeService) -> None:
        actual = service.get_all()

        assert len(actual) == 2
        assert isinstance(actual[0], BaseEntity)
        assert isinstance(actual[1], BaseEntity)

    def test_get_all_empty(self, service: TypeService, mocker: MockerFixture) -> None:
        mocker.patch.object(service._repo, "get_all", return_value=[])

        assert service.get_all() == []
