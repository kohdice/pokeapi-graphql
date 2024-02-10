import pytest

from pokeapi.infrastructure.db.utils import adjust_connection_url


@pytest.mark.parametrize(
    ("connection_url", "expected"),
    [
        (
            "mysql://root:root@db:3306/main_db?charset=utf8",
            "mysql+pymysql://root:root@db:3306/main_db?charset=utf8",
        ),
        (
            "://root:root@db:3306/main_db?charset=utf8",
            "mysql+pymysql://root:root@db:3306/main_db?charset=utf8",
        ),
        (
            "root:root@db:3306/main_db?charset=utf8",
            "mysql+pymysql://root:root@db:3306/main_db?charset=utf8",
        ),
    ],
)
def test_adjust_connection_url(connection_url: str, expected: str) -> None:
    assert adjust_connection_url(connection_url) == expected
