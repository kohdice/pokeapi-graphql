from injector import Injector

from pokeapi.dependencies.context import get_context


def test_get_context() -> None:
    actual = get_context()

    container = actual.get("container")

    assert container is not None
    assert isinstance(container, Injector)
