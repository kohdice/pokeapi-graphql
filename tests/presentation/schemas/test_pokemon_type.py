from unittest.mock import MagicMock

import pytest

from pokeapi.application.services.pokemon_type import TypeService
from pokeapi.exceptions.pokemon_type import TypeNotFoundError
from pokeapi.presentation.schemas.pokemon_type import PokemonType
from tests.conftest import TEST_POKEMON_TYPE_ENTITY

from .conftest import MockInfo

TEST_SCHEMA = PokemonType(id=1, type_name="ノーマル")


class TestPokemonType:
    def test_from_entity(self) -> None:
        assert PokemonType.from_entity(TEST_POKEMON_TYPE_ENTITY) == TEST_SCHEMA

    def test_resolve_node(self, mock_info: MockInfo) -> None:
        mock_info.context["container"].get(TypeService).get_by_id = MagicMock(
            return_value=TEST_POKEMON_TYPE_ENTITY
        )
        actual = PokemonType.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, PokemonType)
        assert actual.id == 1
        assert actual.type_name == "ノーマル"

    def test_resolve_node_type_not_found(self, mock_info: MockInfo) -> None:
        mock_info.context["container"].get(TypeService).get_by_id = MagicMock(
            return_value=None
        )
        with pytest.raises(TypeNotFoundError):
            PokemonType.resolve_node("0", info=mock_info)  # type: ignore
