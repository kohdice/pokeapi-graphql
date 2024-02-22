import pytest
from injector import Injector

from pokeapi.dependencies.di.config import ConfigModule
from pokeapi.dependencies.di.database import DatabaseModule


@pytest.fixture(scope="module")
def dependency_container() -> Injector:
    return Injector([ConfigModule(), DatabaseModule()])
