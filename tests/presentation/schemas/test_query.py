import pytest
from strawberry import Schema

from pokeapi.dependencies.context import get_context
from pokeapi.presentation.schemas.query import Query


class TestQuery:
    # TODO: Fix test
    @pytest.mark.skip(
        reason="It succeeds individually, but fails when considered as a whole."
    )
    def test_pokemon_query(self) -> None:
        query = """
            query testPokemn($id: GlobalID!) {
                pokemon(id: $id) {
                    id
                    nationalPokedexNumber
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
        assert result.data["pokemon"] == {
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

    # TODO: Fix test
    @pytest.mark.skip(
        reason="An error occurred. TypeError: Query fields cannot be resolved."
    )
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

            query testPokemns {
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
