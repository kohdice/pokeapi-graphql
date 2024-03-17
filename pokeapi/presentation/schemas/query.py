from collections.abc import Iterable

import strawberry
from strawberry import relay
from strawberry.types.info import Info

from pokeapi.application.services.pokemon_abc import PokemonServiceABC
from pokeapi.presentation.resolvers.user import get_user_by_token
from pokeapi.presentation.schemas import USER_PAYLOAD
from pokeapi.presentation.schemas.pokemon import Pokemon
from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility
from pokeapi.presentation.schemas.pokemon_type import PokemonType


@strawberry.type(description="Root query schema.")
class Query:
    """Root query schema.

    This schema defines the root query operations.

    Attributes:
        pokemon (Pokemon): Returns a Pokémon resource by ID.
        pokemon_type (PokemonType): Returns a Pokémon Type resource by ID.
        pokemon_ability (PokemonAbility): Returns a Pokémon Ability resource by ID.

    """

    pokemon: Pokemon = relay.node(description="Returns a Pokémon resource by ID.")
    pokemon_type: PokemonType = relay.node(
        description="Returns a Pokémon Type resource by ID."
    )
    pokemon_ability: PokemonAbility = relay.node(
        description="Returns a Pokémon Ability resource by ID."
    )
    user: USER_PAYLOAD = strawberry.field(
        resolver=get_user_by_token,
        description="Returns a User resource by access token.",
    )

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
