import pytest
from freezegun import freeze_time
from strawberry import Schema

from pokeapi.dependencies.context import get_context
from pokeapi.presentation.schemas.query import Query
from tests.conftest import EXECUTION_DATETIME, MockRequest

TEST_RESPONSE_OF_POKEMON = {
    "id": "UG9rZW1vbjox",
    "nationalPokedexNumber": 1,
    "name": "フシギダネ",
    "hp": 45,
    "attack": 49,
    "defense": 49,
    "specialAttack": 65,
    "specialDefense": 65,
    "speed": 45,
    "baseTotal": 318,
    "types": [
        {
            "pokemonType": {"id": "UG9rZW1vblR5cGU6NQ==", "typeName": "くさ"},
            "slot": 1,
        },
        {
            "pokemonType": {"id": "UG9rZW1vblR5cGU6OA==", "typeName": "どく"},
            "slot": 2,
        },
    ],
    "abilities": [
        {
            "pokemonAbility": {
                "id": "UG9rZW1vbkFiaWxpdHk6MzQ=",
                "abilityName": "ようりょくそ",
            },
            "slot": 3,
            "isHidden": True,
        },
        {
            "pokemonAbility": {
                "id": "UG9rZW1vbkFiaWxpdHk6NjU=",
                "abilityName": "しんりょく",
            },
            "slot": 1,
            "isHidden": False,
        },
    ],
}


# TODO: Fix the test to support `strawberry.relay`.
@pytest.mark.skip(
    reason="When testing a Query class that uses strawberry.relay with Schema.execute_sync, it fails."
)
class TestQuery:
    def test_pokemon_query(self) -> None:
        query = """
            query testPokemon($id: GlobalID!) {
                pokemon(id: $id) {
                    id
                    nationalPokedexNumber
                    name
                    hp
                    attack
                    defense
                    specialAttack
                    specialDefense
                    speed
                    baseTotal
                    types {
                        pokemonType {
                        id
                        typeName
                        }
                        slot
                    }
                    abilities {
                        pokemonAbility {
                        id
                        abilityName
                        }
                        slot
                        isHidden
                    }
                }
            }
        """

        schema = Schema(query=Query)
        result = schema.execute_sync(
            query, variable_values={"id": "UG9rZW1vbjox"}, context_value=get_context()
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["pokemon"] == TEST_RESPONSE_OF_POKEMON

    def test_pokemon_by_pokedex_number_query(self) -> None:
        query = """
            query testPokemonByPokedexNumber($pokedexNumber: Int!) {
                pokemonByPokedexNumber(pokedexNumber: $pokedexNumber) {
                    id
                    nationalPokedexNumber
                    name
                    hp
                    attack
                    defense
                    specialAttack
                    specialDefense
                    speed
                    baseTotal
                    types {
                        pokemonType {
                        id
                        typeName
                        }
                        slot
                    }
                    abilities {
                        pokemonAbility {
                        id
                        abilityName
                        }
                        slot
                        isHidden
                    }
                }
            }
        """

        schema = Schema(query=Query)
        result = schema.execute_sync(
            query, variable_values={"pokedexNumber": 1}, context_value=get_context()
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["pokemonByPokedexNumber"] == TEST_RESPONSE_OF_POKEMON

    def test_pokemon_by_name_query(self) -> None:
        query = """
            query testPokemonByName($name: String!) {
                pokemonByName(name: $name) {
                    id
                    nationalPokedexNumber
                    name
                    hp
                    attack
                    defense
                    specialAttack
                    specialDefense
                    speed
                    baseTotal
                    types {
                        pokemonType {
                        id
                        typeName
                        }
                        slot
                    }
                    abilities {
                        pokemonAbility {
                        id
                        abilityName
                        }
                        slot
                        isHidden
                    }
                }
            }
        """

        schema = Schema(query=Query)
        result = schema.execute_sync(
            query, variable_values={"name": "フシギダネ"}, context_value=get_context()
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["pokemonByName"] == TEST_RESPONSE_OF_POKEMON

    def test_pokemons_query(self) -> None:
        query = """
                fragment PokemonInfo on Pokemon {
                    id
                    nationalPokedexNumber
                    name
                    hp
                    attack
                    defense
                    specialAttack
                    specialDefense
                    speed
                    baseTotal
                    types {
                        pokemonType {
                        id
                        typeName
                        }
                        slot
                    }
                    abilities {
                        pokemonAbility {
                        id
                        abilityName
                        }
                        slot
                        isHidden
                    }
                }

            query testPokemons {
                pokemons(first:10) {
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        startCursor
                        endCursor
                    }
                    edges {
                        cursor
                        node {
                            ...PokemonInfo
                        }
                    }
                }
            }
        """

        schema = Schema(query=Query)
        result = schema.execute_sync(query, context_value=get_context())

        assert result.errors is None
        assert result.data is not None
        assert len(result.data["pokemons"]["edges"]) == 2

    def test_type_query(self) -> None:
        query = """
            query testPokemonType($id: GlobalID!) {
                pokemonType(id: $id) {
                    id
                    typeName
                }
            }
        """

        schema = Schema(query=Query)
        result = schema.execute_sync(
            query,
            variable_values={"id": "UG9rZW1vblR5cGU6NQ=="},
            context_value=get_context(),
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["pokemonType"] == {
            "id": "UG9rZW1vblR5cGU6NQ==",
            "typeName": "くさ",
        }

    def test_ability_query(self) -> None:
        query = """
            query testPokemonAbility($id: GlobalID!) {
                pokemonAbility(id: $id) {
                    id
                    abilityName
                }
            }
        """

        schema = Schema(query=Query)
        result = schema.execute_sync(
            query,
            variable_values={"id": "UG9rZW1vbkFiaWxpdHk6NjU="},
            context_value=get_context(),
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["pokemonAbility"] == {
            "id": "UG9rZW1vbkFiaWxpdHk6NjU=",
            "abilityName": "しんりょく",
        }

    @pytest.mark.usefixtures("_setup_token_whitelist_for_user")
    @freeze_time(EXECUTION_DATETIME)
    def test_user_query(self, mock_access_request: MockRequest) -> None:
        query = """
            query testUser {
                user {
                    ... on User {
                        username
                    }
                    ... on UserErrors {
                        message
                    }
                }
            }
        """
        context = get_context()
        context["request"] = mock_access_request
        schema = Schema(query=Query)
        result = schema.execute_sync(query, context_value=context)

        assert result.errors is None
        assert result.data is not None
        assert result.data["user"] == {"username": "Red"}
