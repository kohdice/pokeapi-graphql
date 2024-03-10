from injector import inject, singleton

from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.domain.entities.pokemon_ability import PokemonAbility
from pokeapi.domain.entities.pokemon_stats import PokemonStats
from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.domain.entities.pokemons_ability import PokemonsAbility
from pokeapi.domain.entities.pokemons_type import PokemonsType
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon as PokemonModel
from pokeapi.infrastructure.database.repositories.pokemon import PokemonRepositoryABC


@singleton
class MockPokemonRepository(PokemonRepositoryABC):
    @inject
    def __init__(self) -> None:
        self.__pokemon = PokemonEntity(
            id_=1,
            national_pokedex_number=1,
            name="フシギダネ",
            stats=PokemonStats(
                hp=45,
                attack=49,
                defense=49,
                special_attack=65,
                special_defense=65,
                speed=45,
                base_total=318,
            ),
            pokemons_type=(
                PokemonsType(
                    pokemon_type=PokemonType(
                        id_=5,
                        name="くさ",
                    ),
                    slot=1,
                ),
                PokemonsType(
                    pokemon_type=PokemonType(
                        id_=8,
                        name="どく",
                    ),
                    slot=2,
                ),
            ),
            pokemons_ability=(
                PokemonsAbility(
                    pokemon_ability=PokemonAbility(
                        id_=34,
                        name="ようりょくそ",
                    ),
                    slot=3,
                    is_hidden=True,
                ),
                PokemonsAbility(
                    pokemon_ability=PokemonAbility(
                        id_=65,
                        name="しんりょく",
                    ),
                    slot=1,
                    is_hidden=False,
                ),
            ),
        )

    def _convert_to_entity(self, model: PokemonModel) -> PokemonEntity:  # type: ignore[override]
        return self.__pokemon

    def get_by_id(self, id_: int) -> PokemonEntity | None:
        if id_ < 1:
            return None

        return self.__pokemon

    def get_all(self) -> list[PokemonEntity]:  # type: ignore[override]
        return [self.__pokemon]
