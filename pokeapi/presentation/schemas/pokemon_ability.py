import strawberry
from strawberry import relay
from strawberry.types import Info

from pokeapi.application.services.pokemon_ability import AbilityService
from pokeapi.domain.entities.pokemon_ability import (
    PokemonAbility as PokemonAbilityEntity,
)
from pokeapi.exceptions.pokemon_ability import AbilityNotFoundError


@strawberry.type(description="A schema representing a Pokémon Ability.")
class PokemonAbility(relay.Node):
    """GraphQL schema for Pokémon Ability.

    Attributes:
        id (relay.NodeID): The unique identifier for the Pokémon Ability.
        ability_name (str): Name of Ability.

    """

    id: relay.NodeID[int]
    ability_name: str = strawberry.field(description="Name of this Ability.")

    @classmethod
    def from_entity(cls, entity: PokemonAbilityEntity) -> "PokemonAbility":
        """Create a Pokémon Ability from a Pokémon Ability entity.

        Args:
            entity: The Pokémon Ability entity.

        Returns:
            PokemonAbility: A Pokémon Ability.

        """
        return PokemonAbility(id=entity.id_, ability_name=entity.name)

    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info, required: bool = False
    ) -> "PokemonAbility":
        """Resolve Pokémon Ability.

        Args:
            node_id (str): The unique identifier for the Pokémon Ability.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            PokemonAbility: The Pokémon Ability.

        Raises:
            AbilityNotFoundError: If the Pokémon Ability is not found.

        """
        container = info.context["container"]
        service = container.get(AbilityService)
        entity = service.get_by_id(int(node_id))

        if entity is None:
            raise AbilityNotFoundError("Ability not found")

        return cls.from_entity(entity)
