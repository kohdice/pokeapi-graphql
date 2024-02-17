from collections.abc import Iterable

import strawberry
from strawberry import relay

from pokeapi.presentation.schemas.pokemon import Pokemon


@strawberry.type
class Query:
    """Root query schema.

    This schema defines the root query operations.

    Attributes:
        pokemon (Pokemon): Returns a Pokémon resource by ID.

    """

    pokemon: Pokemon = relay.node(description="Returns a Pokémon resource by ID.")

    @relay.connection(relay.ListConnection[Pokemon], description="List of Pokémon.")
    def pokemons(self) -> Iterable[Pokemon]:
        """Returns a list of Pokémon resources.

        Returns:
            Iterable[Pokemon]: List of Pokémon resources.

        """
        return [
            Pokemon(
                id=1,
                national_pokedex_number=1,
                name="フシギダネ",
                hp=45,
                attack=49,
                defense=49,
                special_attack=65,
                special_defense=65,
                speed=54,
                base_total=318,
            ),
            Pokemon(
                id=2,
                national_pokedex_number=2,
                name="フシギソウ",
                hp=60,
                attack=62,
                defense=63,
                special_attack=80,
                special_defense=80,
                speed=60,
                base_total=405,
            ),
            Pokemon(
                id=3,
                national_pokedex_number=3,
                name="フシギバナ",
                hp=80,
                attack=82,
                defense=83,
                special_attack=100,
                special_defense=100,
                speed=80,
                base_total=525,
            ),
        ]
