from .base import BaseEntity


class PokemonStats(BaseEntity):
    """Value object class of Pokémon's stats.

    Attributes:
        hp (int):   Base stat of HP for this Pokémon.
        attack (int): Base stat of Attack for this Pokémon.
        defense (int): Base stat of Defense for this Pokémon.
        special_attack (int): Base stat of Special Attack for this Pokémon.
        special_defense (int): Base stat of Special Defense for this Pokémon.
        speed (int): Base stat of Special Speed for this Pokémon.
        base_total (int): Base total of stats for this Pokémon.

    """

    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    base_total: int
