import pytest
from injector import Injector

from pokeapi.application.services.pokemon_type import TypeService
from tests.conftest import TEST_POKEMON_TYPE_ENTITY


@pytest.fixture
def service(container: Injector) -> TypeService:
    return container.get(TypeService)


class TestTypeService:
    def test_get_by_id(self, service: TypeService) -> None:
        service._repo.get_by_id.return_value = TEST_POKEMON_TYPE_ENTITY  # type: ignore
        service.get_by_id(1)

    def test_get_by_id_not_found(self, service: TypeService) -> None:
        service._repo.get_by_id.return_value = None  # type: ignore

        assert service.get_by_id(0) is None

    def test_get_all(self, service: TypeService) -> None:
        service._repo.get_all.return_value = [  # type: ignore
            TEST_POKEMON_TYPE_ENTITY,
            TEST_POKEMON_TYPE_ENTITY,
        ]
        actual = service.get_all()

        assert len(actual) == 2

    def test_get_all_empty(self, service: TypeService) -> None:
        service._repo.get_all.return_value = []  # type: ignore

        assert service.get_all() == []
