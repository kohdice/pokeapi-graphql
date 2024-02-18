from pokeapi.domain.entities.base import BaseEntity


class PokemonAbility(BaseEntity):
    """Value object class of Pokémon ability.

    Attributes:
        id_: int: Id of ability.
        name: str: Name of ability.

    """

    id_: int
    name: str
