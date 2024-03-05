from .base import BaseEntity
from .pokemon_type import PokemonType


class PokemonsType(BaseEntity):
    """Value object class of Pokémon's type.

    Attributes:
        pokemon_type (PokemonType): Type of Pokémon's Type
        slot (int): Slot of this Pokémon's Type

    """

    pokemon_type: PokemonType
    slot: int
