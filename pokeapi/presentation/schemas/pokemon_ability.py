import strawberry
from strawberry import relay
from strawberry.types import Info


@strawberry.type
class PokemonAbility(relay.Node):
    """GraphQL schema for Pokémon Ability.

    Attributes:
        id (relay.NodeID): The unique identifier for the Pokémon Ability.
        ability_name (str): Name of Ability.

    """

    id: relay.NodeID[int]
    ability_name: str = strawberry.field(description="Name of this Ability.")

    # TODO: Enable returning data retrieved from the database using the node_id.
    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info | None = None, required: bool = False
    ) -> "PokemonAbility":
        """Resolve Pokémon Ability.

        Args:
            node_id (str): The unique identifier for the Pokémon Ability.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            PokemonAbility: The Pokémon Ability.

        """
        return PokemonAbility(id=1, ability_name="あくしゅう")
