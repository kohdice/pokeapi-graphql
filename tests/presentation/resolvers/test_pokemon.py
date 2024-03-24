from unittest.mock import MagicMock

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.presentation.resolvers.pokemon import (
    get_pokemon_by_name,
    get_pokemon_by_pokedex_number,
)
from pokeapi.presentation.schemas.pokemon import Pokemon
from tests.conftest import TEST_POKEMON_ENTITY, MockInfo


class TestPokemonResolver:
    def test_pokemon(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(PokemonService)
        service.get_by_pokedex_number = MagicMock(return_value=TEST_POKEMON_ENTITY)
        actual = get_pokemon_by_pokedex_number(1, mock_info)  # type: ignore

        assert isinstance(actual, Pokemon)
        assert actual.name == TEST_POKEMON_ENTITY.name
        assert (
            actual.national_pokedex_number
            == TEST_POKEMON_ENTITY.national_pokedex_number
        )

    def test_pokemon_not_found(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(PokemonService)
        service.get_by_pokedex_number = MagicMock(return_value=None)
        actual = get_pokemon_by_pokedex_number(0, mock_info)  # type: ignore

        assert actual is None

    def test_pokemon_by_name(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(PokemonService)
        service.get_by_name = MagicMock(return_value=TEST_POKEMON_ENTITY)
        actual = get_pokemon_by_name(1, mock_info)  # type: ignore

        assert isinstance(actual, Pokemon)
        assert actual.name == TEST_POKEMON_ENTITY.name
        assert (
            actual.national_pokedex_number
            == TEST_POKEMON_ENTITY.national_pokedex_number
        )

    def test_pokemon_by_name_not_found(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(PokemonService)
        service.get_by_name = MagicMock(return_value=None)
        actual = get_pokemon_by_name(0, mock_info)  # type: ignore

        assert actual is None
