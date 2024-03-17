from .base import BaseEntity
from .pokemon_ability import PokemonAbility


class PokemonsAbility(BaseEntity):
    """Value object class of Pokémon's ability.

    Attributes:
        pokemon_ability (PokemonAbility): Ability of Pokémon's Ability
        slot (int): Slot of this Pokémon's Ability
        is_hidden (bool): Whether this Pokémon's ability is a hidden ability

    """

    pokemon_ability: PokemonAbility
    slot: int
    is_hidden: bool
