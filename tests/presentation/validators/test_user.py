import pytest
from pydantic import ValidationError

from pokeapi.presentation.validators.user import UserInputValidator


class TestUserInputValidator:
    @pytest.mark.parametrize(
        ("username", "password"),
        [
            ("Red", "password"),
            ("Green", "12345678"),
            ("1234", "password"),
            ("1234", "12345678"),
            ("Blue123", "password123"),
        ],
    )
    def test_validate(self, username: str, password: str) -> None:
        UserInputValidator(username=username, password=password)

    @pytest.mark.parametrize(
        ("username", "password"),
        [
            ("Red123!", "password1234"),
            ("Red 1234", "password1234"),
            ("あいうえお", "password123"),
            ("ＡＢＣ１２３", "password 123"),
            ("", ""),
        ],
    )
    def test_validate_with_invalid_value(self, username: str, password: str) -> None:
        with pytest.raises(ValidationError):
            UserInputValidator(username=username, password=password)

    @pytest.mark.parametrize(
        ("username", "password"),
        [
            ("R", "password"),
            ("Red", "1"),
            ("R" * 31, "password"),
            ("Red", "1" * 51),
            ("Red", "password" * 10),
        ],
    )
    def test_validate_with_invalid_size(self, username: str, password: str) -> None:
        with pytest.raises(ValidationError):
            UserInputValidator(username=username, password=password)
