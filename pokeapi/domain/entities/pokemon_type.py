from pokeapi.domain.entities.base import BaseEntity


class PokemonType(BaseEntity):
    """Value object class of Pokémon type.

    Attributes:
        id_: int: Id of type.
        name: str: Name of type.

    """

    id_: int
    name: str
