import strawberry
from strawberry import relay
from strawberry.types import Info

from pokeapi.application.services.pokemon_type import TypeService
from pokeapi.domain.entities.pokemon_type import PokemonType as PokemonTypeEntity
from pokeapi.exceptions.pokemon_type import TypeNotFoundError


@strawberry.type
class PokemonType(relay.Node):
    """GraphQL schema for Pokémon Type.

    Attributes:
        id (relay.NodeID): The unique identifier for the Pokémon Type.
        type_name (str): Name of Type.

    """

    id: relay.NodeID[int]
    type_name: str = strawberry.field(description="Name of this Type.")

    @classmethod
    def from_entity(cls, entity: PokemonTypeEntity) -> "PokemonType":
        """Create a Pokémon Type from a Pokémon Type entity.

        Args:
            entity: The Pokémon Type entity.

        Returns:
            PokemonType: A Pokémon Type.

        """
        return PokemonType(id=entity.id_, type_name=entity.name)

    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info, required: bool = False
    ) -> "PokemonType":
        """Resolve Pokémon Type.

        Args:
            node_id (str): The unique identifier for the Pokémon Type.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            PokemonType: The Pokémon Type.

        Raises:
            TypeNotFoundError: If the Pokémon Type is not found.

        """
        container = info.context["container"]
        service = container.get(TypeService)
        entity = service.get_by_id(int(node_id))

        if entity is None:
            raise TypeNotFoundError("Type not found")

        return cls.from_entity(entity)
