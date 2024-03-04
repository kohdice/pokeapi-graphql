import pytest
from injector import Injector

from pokeapi.dependencies.di.config import ConfigModule


@pytest.fixture(scope="module")
def dependency_container() -> Injector:
    return Injector([ConfigModule()])
