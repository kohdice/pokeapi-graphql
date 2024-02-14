import strawberry
from strawberry import relay
from strawberry.types import Info

from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility


@strawberry.type
class PokemonsAbility(relay.Node):
    """GraphQL schema for Pokémon's Ability.

    Attributes:
        id (relay.NodeID): The unique identifier for the Pokémon's Ability.
        pokemon_ability (PokemonAbility): Ability of Pokémon's Ability
        slot (int): Slot of this Pokémon's Ability
        is_hidden (bool): Whether this Pokémon's ability is a hidden ability

    """

    id: relay.NodeID[str]
    pokemon_ability: PokemonAbility = strawberry.field(
        description="Ability of this Pokémon Ability"
    )
    slot: int = strawberry.field(description="Slot of this Pokémon's Ability")
    is_hidden: bool = strawberry.field(
        description="Whether this Pokémon's ability is a hidden ability"
    )

    # TODO: Enable returning data retrieved from the database using the node_id.
    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info | None = None, required: bool = False
    ):
        """Resolve Pokémon's Ability.

        Args:
            node_id (str): The unique identifier for the Pokémon's Ability.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            PokemonsAbility: The Pokémon's Ability.

        """
        return PokemonsAbility(
            id="1",
            pokemon_ability=PokemonAbility(id=1, ability_name="あくしゅう"),
            slot=1,
            is_hidden=False,
        )
