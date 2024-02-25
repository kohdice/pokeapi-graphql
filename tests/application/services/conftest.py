import pytest
from injector import Binder, Injector, singleton

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.domain.repositories.pokemon_type import TypeRepositoryABC
from pokeapi.infrastructure.database.models import BaseModel


class MockEntity(BaseEntity):
    id_: int
    name: str


class MockRepository(PokemonRepositoryABC, TypeRepositoryABC):
    def _convert_to_entity(self, model: BaseModel) -> BaseEntity:
        return BaseEntity()

    def get_by_id(self, id_: int) -> MockEntity | None:
        if id_ < 1:
            return None

        return MockEntity(id_=id_, name="mock")

    def get_all(self) -> list[MockEntity]:  # type: ignore[override]
        return [
            MockEntity(id_=1, name="mock_1"),
            MockEntity(id_=2, name="mock_2"),
        ]


@pytest.fixture(scope="module")
def dependency_container() -> Injector:
    def configure(binder: Binder) -> None:
        binder.bind(PokemonRepositoryABC, to=MockRepository, scope=singleton)  # type: ignore[type-abstract]
        binder.bind(TypeRepositoryABC, to=MockRepository, scope=singleton)  # type: ignore[type-abstract]

    return Injector(configure)
