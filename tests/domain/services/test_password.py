import pytest
from passlib.hash import argon2

from pokeapi.domain.services.password import PasswordService


@pytest.fixture(scope="module")
def hashed_password() -> str:
    hashed = argon2.hash("password")
    assert isinstance(hashed, str)

    return hashed


class TestPasswordService:
    def test_hash(self) -> None:
        actual = PasswordService.hash("password")

        assert isinstance(actual, str)

    @pytest.mark.usefixtures("hashed_password")
    @pytest.mark.parametrize(
        ("password", "expected"),
        [("password", True), ("hoge", False)],
    )
    def test_verify(self, hashed_password: str, password: str, expected: bool) -> None:
        actual = PasswordService.verify(password, hashed_password)

        assert actual is expected
