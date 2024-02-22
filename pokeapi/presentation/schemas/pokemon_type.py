import strawberry
from strawberry import relay
from strawberry.types import Info


@strawberry.type
class PokemonType(relay.Node):
    """GraphQL schema for Pokémon Type.

    Attributes:
        id (relay.NodeID): The unique identifier for the Pokémon Type.
        type_name (str): Name of Type.

    """

    id: relay.NodeID[int]
    type_name: str = strawberry.field(description="Name of this Type.")

    # TODO: Enable returning data retrieved from the database using the node_id.
    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info | None = None, required: bool = False
    ) -> "PokemonType":
        """Resolve Pokémon Type.

        Args:
            node_id (str): The unique identifier for the Pokémon Type.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            PokemonType: The Pokémon Type.

        """
        return PokemonType(id=1, type_name="ノーマル")
