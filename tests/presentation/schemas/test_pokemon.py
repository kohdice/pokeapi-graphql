import pytest

from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.domain.entities.pokemon_ability import (
    PokemonAbility as PokemonAbilityEntity,
)
from pokeapi.domain.entities.pokemon_stats import PokemonStats
from pokeapi.domain.entities.pokemon_type import PokemonType as PokemonTypeEntity
from pokeapi.domain.entities.pokemons_ability import (
    PokemonsAbility as PokemonsAbilityEntity,
)
from pokeapi.domain.entities.pokemons_type import PokemonsType as PokemonsTypeEntity
from pokeapi.exceptions.pokemon import PokemonNotFoundError
from pokeapi.presentation.schemas.pokemon import Pokemon as PokemonSchema
from pokeapi.presentation.schemas.pokemon_ability import (
    PokemonAbility as PokemonAbilitySchema,
)
from pokeapi.presentation.schemas.pokemon_type import PokemonType as PokemonTypeSchema
from pokeapi.presentation.schemas.pokemons_ability import (
    PokemonsAbility as PokemonsAbilitySchema,
)
from pokeapi.presentation.schemas.pokemons_type import (
    PokemonsType as PokemonsTypeSchema,
)

from .conftest import MockInfo

TEST_ENTITY = PokemonEntity(
    id_=1,
    national_pokedex_number=1,
    name="フシギダネ",
    stats=PokemonStats(
        hp=45,
        attack=49,
        defense=49,
        special_attack=65,
        special_defense=65,
        speed=45,
        base_total=318,
    ),
    pokemons_type=(
        PokemonsTypeEntity(
            pokemon_type=PokemonTypeEntity(
                id_=5,
                name="くさ",
            ),
            slot=1,
        ),
        PokemonsTypeEntity(
            pokemon_type=PokemonTypeEntity(
                id_=8,
                name="どく",
            ),
            slot=2,
        ),
    ),
    pokemons_ability=(
        PokemonsAbilityEntity(
            pokemon_ability=PokemonAbilityEntity(
                id_=34,
                name="ようりょくそ",
            ),
            slot=3,
            is_hidden=True,
        ),
        PokemonsAbilityEntity(
            pokemon_ability=PokemonAbilityEntity(
                id_=65,
                name="しんりょく",
            ),
            slot=1,
            is_hidden=False,
        ),
    ),
)

TEST_SCHEMA = PokemonSchema(
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
        PokemonsTypeSchema(
            pokemon_type=PokemonTypeSchema(id=5, type_name="くさ"), slot=1
        ),
        PokemonsTypeSchema(
            pokemon_type=PokemonTypeSchema(id=8, type_name="どく"), slot=2
        ),
    ],
    abilities=[
        PokemonsAbilitySchema(
            pokemon_ability=PokemonAbilitySchema(id=34, ability_name="ようりょくそ"),
            slot=3,
            is_hidden=True,
        ),
        PokemonsAbilitySchema(
            pokemon_ability=PokemonAbilitySchema(id=65, ability_name="しんりょく"),
            slot=1,
            is_hidden=False,
        ),
    ],
)


class TestPokemonSchema:
    def test_from_entity(self) -> None:
        assert PokemonSchema.from_entity(TEST_ENTITY) == TEST_SCHEMA

    def test_resolve_node(self, mock_info: MockInfo) -> None:
        actual = PokemonSchema.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, PokemonSchema)
        assert actual.id == 1
        assert actual.types == [
            PokemonsTypeSchema(
                pokemon_type=PokemonTypeSchema(id=1, type_name="1"), slot=1
            ),
            PokemonsTypeSchema(
                pokemon_type=PokemonTypeSchema(id=2, type_name="2"), slot=2
            ),
        ]
        assert actual.abilities == [
            PokemonsAbilitySchema(
                pokemon_ability=PokemonAbilitySchema(id=1, ability_name="1"),
                slot=1,
                is_hidden=False,
            ),
            PokemonsAbilitySchema(
                pokemon_ability=PokemonAbilitySchema(id=2, ability_name="2"),
                slot=2,
                is_hidden=True,
            ),
        ]

    def test_resolve_node_not_found(self, mock_info: MockInfo) -> None:
        with pytest.raises(PokemonNotFoundError):
            PokemonSchema.resolve_node("0", info=mock_info)  # type: ignore
