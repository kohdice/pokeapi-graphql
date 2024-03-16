import pytest
from passlib.hash import argon2

from pokeapi.domain.services.password import PasswordService


@pytest.fixture(scope="module")
def service() -> PasswordService:
    return PasswordService()


@pytest.fixture(scope="module")
def hashed_password() -> str:
    hashed = argon2.hash("password")
    assert isinstance(hashed, str)

    return hashed


class TestPasswordService:
    def test_hash(self, service: PasswordService) -> None:
        service.hash("password")

    @pytest.mark.usefixtures("hashed_password")
    @pytest.mark.parametrize(
        ("password", "expected"),
        [("password", True), ("hoge", False)],
    )
    def test_verify(
        self,
        service: PasswordService,
        hashed_password: str,
        password: str,
        expected: bool,
    ) -> None:
        actual = service.verify(password, hashed_password)

        assert actual is expected
