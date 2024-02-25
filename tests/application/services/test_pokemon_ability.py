import pytest
from injector import Injector
from pytest_mock import MockerFixture

from pokeapi.application.services.pokemon_ability import AbilityService
from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.repositories.pokemon_ability import AbilityRepositoryABC


@pytest.fixture()
def service(dependency_container: Injector) -> AbilityService:
    repo = dependency_container.get(AbilityRepositoryABC)  # type: ignore[type-abstract]

    return AbilityService(repo)


class TestAbilityService:
    @pytest.mark.parametrize("id_", [1, 2])
    def test_get_by_id(self, service: AbilityService, id_: int) -> None:
        actual = service.get_by_id(id_)

        assert isinstance(actual, BaseEntity)

    def test_get_by_id_not_found(self, service: AbilityService) -> None:
        assert service.get_by_id(0) is None

    def test_get_all(self, service: AbilityService) -> None:
        actual = service.get_all()

        assert len(actual) == 2
        assert isinstance(actual[0], BaseEntity)
        assert isinstance(actual[1], BaseEntity)

    def test_get_all_empty(
        self, service: AbilityService, mocker: MockerFixture
    ) -> None:
        mocker.patch.object(service._repo, "get_all", return_value=[])

        assert service.get_all() == []
