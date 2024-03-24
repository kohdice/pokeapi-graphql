from strawberry.types.info import Info

from pokeapi.application.services.pokemon import PokemonService
from pokeapi.presentation.schemas.pokemon import Pokemon


def get_pokemon_by_pokedex_number(pokedex_number: int, info: Info) -> Pokemon | None:
    """Retrieves a Pokemon by Pokedex number.

    Args:
        pokedex_number (int): The Pokedex number.
        info (Info): The query info.

    Returns:
        Pokemon | None: The result of the operation.

    """
    container = info.context.get("container")
    service = container.get(PokemonService)
    pokemon = service.get_by_pokedex_number(pokedex_number)

    if pokemon is None:
        return None

    return Pokemon.from_entity(pokemon)
