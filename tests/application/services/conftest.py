import pytest
from injector import Binder, Injector, singleton

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.infrastructure.database.models import BaseModel


class MockPokemonEntity(BaseEntity):
    id_: int
    name: str


class MockPokemonRepository(PokemonRepositoryABC):
    def _convert_to_entity(self, model: BaseModel) -> BaseEntity:
        return BaseEntity()

    def get_by_id(self, id_: int) -> MockPokemonEntity | None:
        if id_ < 1:
            return None

        return MockPokemonEntity(id_=id_, name="mock")

    def get_all(self) -> list[MockPokemonEntity]:  # type: ignore[override]
        return [
            MockPokemonEntity(id_=1, name="mock_1"),
            MockPokemonEntity(id_=2, name="mock_2"),
        ]


@pytest.fixture(scope="module")
def dependency_container() -> Injector:
    def configure(binder: Binder) -> None:
        binder.bind(PokemonRepositoryABC, to=MockPokemonRepository, scope=singleton)  # type: ignore[type-abstract]

    return Injector(configure)
