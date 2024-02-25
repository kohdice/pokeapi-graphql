from collections.abc import Iterable

import strawberry
from strawberry import relay
from strawberry.types.info import Info

from pokeapi.application.services.pokemon_abc import PokemonServiceABC
from pokeapi.presentation.schemas.pokemon import Pokemon


@strawberry.type
class Query:
    """Root query schema.

    This schema defines the root query operations.

    Attributes:
        pokemon (Pokemon): Returns a Pokémon resource by ID.

    """

    pokemon: Pokemon = relay.node(description="Returns a Pokémon resource by ID.")

    # TODO: Fix test it.
    @relay.connection(relay.ListConnection[Pokemon], description="List of Pokémon.")
    def pokemons(self, info: Info) -> Iterable[Pokemon]:  # pragma: no cover
        """Returns a list of Pokémon resources.

        Returns:
            Iterable[Pokemon]: A list of Pokémon resources.

        """
        container = info.context["container"]
        service = container.get(PokemonServiceABC)
        entities = service.get_all()

        return [Pokemon.from_entity(entity) for entity in entities]
