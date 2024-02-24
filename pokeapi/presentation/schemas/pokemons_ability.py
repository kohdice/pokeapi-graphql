import strawberry

from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility


@strawberry.type
class PokemonsAbility:
    """GraphQL schema for Pokémon's Ability.

    Attributes:
        pokemon_ability (PokemonAbility): Ability of Pokémon's Ability
        slot (int): Slot of this Pokémon's Ability
        is_hidden (bool): Whether this Pokémon's ability is a hidden ability

    """

    pokemon_ability: PokemonAbility = strawberry.field(
        description="Ability of this Pokémon Ability"
    )
    slot: int = strawberry.field(description="Slot of this Pokémon's Ability")
    is_hidden: bool = strawberry.field(
        description="Whether this Pokémon's ability is a hidden ability"
    )
