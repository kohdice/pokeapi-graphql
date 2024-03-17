from .base import BaseEntity
from .pokemon_stats import PokemonStats
from .pokemons_ability import PokemonsAbility
from .pokemons_type import PokemonsType


class Pokemon(BaseEntity):
    """Entity class of Pokémon.

    Attributes:
        id_ (int): The unique identifier for the Pokémon.
        national_pokedex_number (int): The National Pokédex number of this Pokémon.
        name (str): The name of this Pokémon.
        stats (PokemonStats): The base stats of this Pokémon.
        pokemons_type (tuple): A tuple containing PokemonsType object for this Pokémon.
        pokemons_ability (tuple): A tuple containing PokemonsAbility object for this Pokémon.

    """

    id_: int
    national_pokedex_number: int
    name: str
    stats: PokemonStats
    pokemons_type: tuple[PokemonsType, ...]
    pokemons_ability: tuple[PokemonsAbility, ...]
