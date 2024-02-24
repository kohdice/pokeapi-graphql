import strawberry
from strawberry import relay
from strawberry.types import Info

from pokeapi.application.services.pokemon_abc import PokemonServiceABC
from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.exceptions.pokemon import PokemonNotFoundError
from pokeapi.presentation.schemas.pokemon_ability import PokemonAbility
from pokeapi.presentation.schemas.pokemon_type import PokemonType
from pokeapi.presentation.schemas.pokemons_ability import PokemonsAbility
from pokeapi.presentation.schemas.pokemons_type import PokemonsType


@strawberry.type
class Pokemon(relay.Node):
    """GraphQL schema for Pokémon.

    Attributes:
        id (relay.NodeID): The unique identifier for the Pokémon.
        national_pokedex_number (int): The national pokedex number of the Pokémon.
        name (str): The name of Pokémon.
        hp (int):   Base stat of HP for this Pokémon.
        attack (int): Base stat of Attack for this Pokémon.
        defense (int): Base stat of Defense for this Pokémon.
        special_attack (int): Base stat of Special Attack for this Pokémon.
        special_defense (int): Base stat of Special Defense for this Pokémon.
        speed (int): Base stat of Special Speed for this Pokémon.
        base_total (int): Base total of stats for this Pokémon.

    """

    id: relay.NodeID[int]
    national_pokedex_number: int = strawberry.field(
        description="The national pokedex number of the Pokémon."
    )
    name: str = strawberry.field(description="The name of Pokémon.")
    hp: int = strawberry.field(description="Base stat of HP for this Pokémon.")
    attack: int = strawberry.field(description="Base stat of Attack for this Pokémon.")
    defense: int = strawberry.field(
        description="Base stat of Defense for this Pokémon."
    )
    special_attack: int = strawberry.field(
        description="Base stat of Special Attack for this Pokémon."
    )
    special_defense: int = strawberry.field(
        description="Base stat of Special Defense for this Pokémon."
    )
    speed: int = strawberry.field(
        description="Base stat of Special Speed for this Pokémon."
    )
    base_total: int = strawberry.field(
        description="Base total of stats for this Pokémon."
    )
    types: list[PokemonsType] = strawberry.field(description="Type of Pokémon's Type")
    abilities: list[PokemonsAbility] = strawberry.field(
        description="Ability of Pokémon's Ability"
    )

    @classmethod
    def from_entity(cls, entity: PokemonEntity) -> "Pokemon":
        """Create a Pokémon schema from a Pokémon entity.

        Args:
            entity (PokemonEntity): The Pokémon entity.

        Returns:
            Pokemon: The Pokémon schema.

        """
        types = [
            PokemonsType(
                pokemon_type=PokemonType(
                    id=type_.pokemon_type.id_, type_name=type_.pokemon_type.name
                ),
                slot=type_.slot,
            )
            for type_ in entity.pokemons_type
        ]
        abilities = [
            PokemonsAbility(
                pokemon_ability=PokemonAbility(
                    id=ability.pokemon_ability.id_,
                    ability_name=ability.pokemon_ability.name,
                ),
                slot=ability.slot,
                is_hidden=ability.is_hidden,
            )
            for ability in entity.pokemons_ability
        ]
        return cls(
            id=entity.id_,
            national_pokedex_number=entity.national_pokedex_number,
            name=entity.name,
            hp=entity.stats.hp,
            attack=entity.stats.attack,
            defense=entity.stats.defense,
            special_attack=entity.stats.special_attack,
            special_defense=entity.stats.special_defense,
            speed=entity.stats.speed,
            base_total=entity.stats.base_total,
            types=types,
            abilities=abilities,
        )

    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info, required: bool = False
    ) -> "Pokemon":
        """Resolve Pokémon by node_id.

        Args:
            node_id (str): The unique identifier for the Pokémon.
            info (Info): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            Pokemon: The Pokémon schema.

        Raises:
            PokemonNotFoundError: If the Pokémon is not found.

        """
        container = info.context["container"]
        service = container.get(PokemonServiceABC)
        entity = service.get_by_id(int(node_id))

        if entity is None:
            raise PokemonNotFoundError("Pokemon not found")

        return cls.from_entity(entity)
