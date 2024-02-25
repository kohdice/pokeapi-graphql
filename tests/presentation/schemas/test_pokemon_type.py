import pytest

from pokeapi.domain.entities.pokemon_type import PokemonType as PokemonTypeEntity
from pokeapi.exceptions.pokemon_type import TypeNotFoundError
from pokeapi.presentation.schemas.pokemon_type import PokemonType as PokemonTypeSchema

from .conftest import MockInfo

TEST_ENTITY = PokemonTypeEntity(
    id_=1,
    name="ノーマル",
)

TEST_SCHEMA = PokemonTypeSchema(
    id=1,
    type_name="ノーマル",
)


class TestPokemonType:
    def test_from_entity(self) -> None:
        assert PokemonTypeSchema.from_entity(TEST_ENTITY) == TEST_SCHEMA

    def test_resolve_node(self, mock_info: MockInfo) -> None:
        actual = PokemonTypeSchema.resolve_node("1", info=mock_info)  # type: ignore

        assert isinstance(actual, PokemonTypeSchema)
        assert actual.id == 1
        assert actual.type_name == "mock_1"

    def test_resolve_node_type_not_found(self, mock_info: MockInfo) -> None:
        with pytest.raises(TypeNotFoundError):
            PokemonTypeSchema.resolve_node("0", info=mock_info)  # type: ignore
