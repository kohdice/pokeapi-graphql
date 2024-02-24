import strawberry

from pokeapi.presentation.schemas.pokemon_type import PokemonType


@strawberry.type
class PokemonsType:
    """GraphQL schema for Pokémon's Type.

    Attributes:
        pokemon_type (PokemonType): Type of Pokémon's Type
        slot (int): Slot of this Pokémon's Type

    """

    pokemon_type: PokemonType = strawberry.field(
        description="Ability of this Pokémon's Type"
    )
    slot: int = strawberry.field(description="Slot of this Pokémon's type")
