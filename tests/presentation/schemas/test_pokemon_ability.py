from unittest.mock import MagicMock

import pytest

from pokeapi.application.services.pokemon_ability import AbilityService
from pokeapi.exceptions.pokemon_ability import AbilityNotFoundError
from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility
from tests.conftest import TEST_POKEMON_ABILITY_ENTITY, MockInfo

TEST_SCHEMA = PokemonAbility(id=1, ability_name="あくしゅう")


class TestPokemonType:
    def test_from_entity(self) -> None:
        assert PokemonAbility.from_entity(TEST_POKEMON_ABILITY_ENTITY) == TEST_SCHEMA

    def test_resolve_node(self, mock_info: MockInfo) -> None:
        mock_info.context["container"].get(AbilityService).get_by_id = MagicMock(
            return_value=TEST_POKEMON_ABILITY_ENTITY
        )
        actual = PokemonAbility.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, PokemonAbility)
        assert actual.id == 1
        assert actual.ability_name == "あくしゅう"

    def test_resolve_node_type_not_found(self, mock_info: MockInfo) -> None:
        mock_info.context["container"].get(AbilityService).get_by_id = MagicMock(
            return_value=None
        )
        with pytest.raises(AbilityNotFoundError):
            PokemonAbility.resolve_node("0", info=mock_info)  # type: ignore
