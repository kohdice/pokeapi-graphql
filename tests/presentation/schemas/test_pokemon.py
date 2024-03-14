from unittest.mock import MagicMock

import pytest

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.exceptions.pokemon import PokemonNotFoundError
from pokeapi.presentation.schemas.pokemon import Pokemon
from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility
from pokeapi.presentation.schemas.pokemon_type import PokemonType
from pokeapi.presentation.schemas.pokemons_ability import PokemonsAbility
from pokeapi.presentation.schemas.pokemons_type import PokemonsType
from tests.conftest import TEST_POKEMON_ENTITY, MockInfo

TEST_SCHEMA = Pokemon(
    id=1,
    national_pokedex_number=1,
    name="フシギダネ",
    hp=45,
    attack=49,
    defense=49,
    special_attack=65,
    special_defense=65,
    speed=45,
    base_total=318,
    types=[
        PokemonsType(pokemon_type=PokemonType(id=5, type_name="くさ"), slot=1),
        PokemonsType(pokemon_type=PokemonType(id=8, type_name="どく"), slot=2),
    ],
    abilities=[
        PokemonsAbility(
            pokemon_ability=PokemonAbility(id=34, ability_name="ようりょくそ"),
            slot=3,
            is_hidden=True,
        ),
        PokemonsAbility(
            pokemon_ability=PokemonAbility(id=65, ability_name="しんりょく"),
            slot=1,
            is_hidden=False,
        ),
    ],
)


class TestPokemonSchema:
    def test_from_entity(self) -> None:
        assert Pokemon.from_entity(TEST_POKEMON_ENTITY) == TEST_SCHEMA

    def test_resolve_node(self, mock_info: MockInfo) -> None:
        mock_info.context["container"].get(PokemonService).get_by_id = MagicMock(
            return_value=TEST_POKEMON_ENTITY
        )
        actual = Pokemon.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, Pokemon)
        assert actual.id == 1
        assert actual.types == [
            PokemonsType(pokemon_type=PokemonType(id=5, type_name="くさ"), slot=1),
            PokemonsType(pokemon_type=PokemonType(id=8, type_name="どく"), slot=2),
        ]
        assert actual.abilities == [
            PokemonsAbility(
                pokemon_ability=PokemonAbility(id=34, ability_name="ようりょくそ"),
                slot=3,
                is_hidden=True,
            ),
            PokemonsAbility(
                pokemon_ability=PokemonAbility(id=65, ability_name="しんりょく"),
                slot=1,
                is_hidden=False,
            ),
        ]

    def test_resolve_node_not_found(self, mock_info: MockInfo) -> None:
        mock_info.context["container"].get(PokemonService).get_by_id = MagicMock(
            return_value=None
        )
        with pytest.raises(PokemonNotFoundError):
            Pokemon.resolve_node("0", info=mock_info)  # type: ignore
