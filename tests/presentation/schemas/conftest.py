from dataclasses import dataclass

import pytest
from injector import Binder, Injector, singleton
from starlette.responses import Response

from pokeapi.application.services.pokemon_abc import PokemonServiceABC
from pokeapi.domain.entities.base import BaseEntity


class MockStats(BaseEntity):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    base_total: int


class MockEntity(BaseEntity):
    id_: int
    national_pokedex_number: int
    name: str
    stats: MockStats
    pokemons_type: tuple
    pokemons_ability: tuple


class MockType(BaseEntity):
    id_: int
    name: str


class MockTypes(BaseEntity):
    pokemon_type: MockType
    slot: int


class MockAbility(BaseEntity):
    id_: int
    name: str


class MockAbilities(BaseEntity):
    pokemon_ability: MockAbility
    slot: int
    is_hidden: bool


def create_entity(id_: int) -> MockEntity:
    stats = MockStats(
        hp=id_,
        attack=id_,
        defense=id_,
        special_attack=id_,
        special_defense=id_,
        speed=id_,
        base_total=id_ * 6,
    )

    pokemons_type = (
        MockTypes(pokemon_type=MockType(id_=type_, name=str(type_)), slot=type_)
        for type_ in [id_, id_ + 1]
    )

    pokemons_ability = (
        MockAbilities(
            pokemon_ability=MockAbility(id_=ability, name=str(ability)),
            slot=ability,
            is_hidden=is_hidden,
        )
        for ability, is_hidden in [(id_, False), (id_ + 1, True)]
    )

    return MockEntity(
        id_=id_,
        national_pokedex_number=id_,
        name=f"mock_{id_}",
        stats=stats,
        pokemons_type=pokemons_type,
        pokemons_ability=pokemons_ability,
    )


class MockPokemonService(PokemonServiceABC):
    def get_by_id(self, id_: int) -> MockEntity | None:
        if id_ < 1:
            return None

        return create_entity(id_)

    def get_all(self) -> list[MockEntity]:  # type: ignore[override]
        return [
            create_entity(1),
            create_entity(2),
        ]


class MockRequest:
    pass


@dataclass
class MockInfo:
    context: dict


@pytest.fixture(scope="module")
def dependency_container() -> Injector:
    def configure(binder: Binder) -> None:
        binder.bind(PokemonServiceABC, to=MockPokemonService, scope=singleton)  # type: ignore[type-abstract]

    return Injector(configure)


@pytest.fixture(scope="module")
def mock_info(dependency_container: Injector) -> MockInfo:
    return MockInfo(
        context={
            "container": dependency_container,
            "request": MockRequest(),
            "response": Response(),
        }
    )
