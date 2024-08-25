import pytest
from injector import Injector

from pokeapi.application.services.pokemon import PokemonService
from tests.conftest import TEST_POKEMON_ENTITY


@pytest.fixture
def service(container: Injector) -> PokemonService:
    return container.get(PokemonService)


class TestPokemonService:
    def test_get_by_id(self, service: PokemonService) -> None:
        service._repo.get_by_id.return_value = TEST_POKEMON_ENTITY  # type: ignore
        service.get_by_id(1)

    def test_get_by_id_not_found(self, service: PokemonService) -> None:
        service._repo.get_by_id.return_value = None  # type: ignore

        assert service.get_by_id(0) is None

    def test_get_by_pokedex_number(self, service: PokemonService) -> None:
        service._repo.get_by_pokedex_number.return_value = TEST_POKEMON_ENTITY  # type: ignore
        service.get_by_pokedex_number(1)

    def test_get_by_pokedex_number_not_found(self, service: PokemonService) -> None:
        service._repo.get_by_pokedex_number.return_value = None  # type: ignore

        assert service.get_by_pokedex_number(0) is None

    def test_get_by_name(self, service: PokemonService) -> None:
        service._repo.get_by_name.return_value = TEST_POKEMON_ENTITY  # type: ignore
        service.get_by_name("フシギダネ")

    def test_get_by_name_not_found(self, service: PokemonService) -> None:
        service._repo.get_by_name.return_value = None  # type: ignore

        assert service.get_by_name("けつばん") is None

    def test_get_all(self, service: PokemonService) -> None:
        service._repo.get_all.return_value = [TEST_POKEMON_ENTITY, TEST_POKEMON_ENTITY]  # type: ignore
        actual = service.get_all()

        assert len(actual) == 2

    def test_get_all_empty(self, service: PokemonService) -> None:
        service._repo.get_all.return_value = []  # type: ignore

        assert service.get_all() == []
