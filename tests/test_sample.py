from pokeapi.main import sample


def test_sample() -> None:
    assert sample(1, 2) == 3
