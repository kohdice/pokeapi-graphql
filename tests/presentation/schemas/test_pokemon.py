import pytest

from pokeapi.exceptions.pokemon import PokemonNotFoundError
from pokeapi.presentation.schemas.pokemon import Pokemon
from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility
from pokeapi.presentation.schemas.pokemon_type import PokemonType
from pokeapi.presentation.schemas.pokemons_ability import PokemonsAbility
from pokeapi.presentation.schemas.pokemons_type import PokemonsType

from .conftest import MockInfo


class TestPokemonSchema:
    def test_resolve_node(self, mock_info: MockInfo) -> None:
        actual = Pokemon.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, Pokemon)
        assert actual.id == 1
        assert actual.types == [
            PokemonsType(pokemon_type=PokemonType(id=1, type_name="1"), slot=1),
            PokemonsType(pokemon_type=PokemonType(id=2, type_name="2"), slot=2),
        ]
        assert actual.abilities == [
            PokemonsAbility(
                pokemon_ability=PokemonAbility(id=1, ability_name="1"),
                slot=1,
                is_hidden=False,
            ),
            PokemonsAbility(
                pokemon_ability=PokemonAbility(id=2, ability_name="2"),
                slot=2,
                is_hidden=True,
            ),
        ]

    def test_resolve_node_not_found(self, mock_info: MockInfo) -> None:
        with pytest.raises(PokemonNotFoundError):
            Pokemon.resolve_node("0", info=mock_info)  # type: ignore
