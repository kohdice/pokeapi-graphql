import strawberry
from strawberry import relay
from strawberry.types import Info

from pokeapi.presentation.schemas.pokemon_type import PokemonType


@strawberry.type
class PokemonsType(relay.Node):
    """GraphQL schema for Pokémon's Type.

    Attributes:
        pokemon_type (PokemonType): Type of Pokémon's Type
        slot (int): Slot of this Pokémon's Type

    """

    id: relay.NodeID[str]
    pokemon_type: PokemonType = strawberry.field(
        description="Ability of this Pokémon's Type"
    )
    slot: int = strawberry.field(description="Slot of this Pokémon's type")

    # TODO: Enable returning data retrieved from the database using the node_id.
    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info | None = None, required: bool = False
    ):
        """Resolve Pokémon's Type.

        Args:
            node_id (str): The unique identifier for the Pokémon's Type.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            PokemonsType: The Pokémon's Type.

        """
        return PokemonsType(
            id=node_id, pokemon_type=PokemonType(id=1, type_name="ノーマル"), slot=1
        )
