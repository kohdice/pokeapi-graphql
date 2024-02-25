import pytest

from pokeapi.domain.entities.pokemon_ability import (
    PokemonAbility as PokemonAbilityEntity,
)
from pokeapi.exceptions.pokemon_ability import AbilityNotFoundError
from pokeapi.presentation.schemas.pokemon_ability import (
    PokemonAbility as PokemonAbilitySchema,
)

from .conftest import MockInfo

TEST_ENTITY = PokemonAbilityEntity(
    id_=1,
    name="あくしゅう",
)

TEST_SCHEMA = PokemonAbilitySchema(
    id=1,
    ability_name="あくしゅう",
)


class TestPokemonType:
    def test_from_entity(self) -> None:
        assert PokemonAbilitySchema.from_entity(TEST_ENTITY) == TEST_SCHEMA

    def test_resolve_node(self, mock_info: MockInfo) -> None:
        actual = PokemonAbilitySchema.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, PokemonAbilitySchema)
        assert actual.id == 1
        assert actual.ability_name == "mock_1"

    def test_resolve_node_type_not_found(self, mock_info: MockInfo) -> None:
        with pytest.raises(AbilityNotFoundError):
            PokemonAbilitySchema.resolve_node("0", info=mock_info)  # type: ignore
