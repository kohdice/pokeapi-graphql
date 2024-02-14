from collections.abc import Iterable

import strawberry
from strawberry import relay
from strawberry.types import Info

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

    @classmethod
    def resolve_node(
        cls, node_id: str, *, info: Info | None = None, required: bool = False
    ):
        """Resolve Pokémon by node_id.

        Args:
            node_id (str): The unique identifier for the Pokémon.
            info (Info, optional): Information about the execution of the query.
            required (bool, optional): Whether the node is required.

        Returns:
            Pokemon: The Pokémon.

        """
        return Pokemon(
            id=1,
            national_pokedex_number=1,
            name="フシギダネ",
            hp=45,
            attack=49,
            defense=49,
            special_attack=65,
            special_defense=65,
            speed=54,
            base_total=318,
        )

    @relay.connection(
        relay.ListConnection[PokemonsType], description="Type of this Pokémon."
    )
    def pokemons_type(self) -> Iterable[PokemonsType]:
        """Return the type of this Pokémon.

        Returns:
            Iterable[PokemonsType]: Type of this Pokémon.

        """
        return [
            PokemonsType(
                id="1-5", pokemon_type=PokemonType(id=5, type_name="くさ"), slot=1
            ),
            PokemonsType(
                id="1-8", pokemon_type=PokemonType(id=8, type_name="どく"), slot=2
            ),
        ]

    @relay.connection(
        relay.ListConnection[PokemonsAbility], description="Ability of this Pokémon."
    )
    def pokemons_ability(self) -> Iterable[PokemonsAbility]:
        """Return the ability of this Pokémon.

        Returns:
            Iterable[PokemonsAbility]: Ability of this Pokémon.

        """
        return [
            PokemonsAbility(
                id="1-65",
                pokemon_ability=PokemonAbility(id=65, ability_name="しんりょく"),
                slot=1,
                is_hidden=False,
            ),
            PokemonsAbility(
                id="1-34",
                pokemon_ability=PokemonAbility(id=34, ability_name="ようりょくそ"),
                slot=3,
                is_hidden=True,
            ),
        ]
