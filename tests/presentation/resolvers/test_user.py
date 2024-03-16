from unittest.mock import MagicMock

from pokeapi.application.services.user import UserService
from pokeapi.exceptions.token import TokenVerificationError
from pokeapi.exceptions.user import UserCreationError
from pokeapi.presentation.resolvers.user import create_user, get_user_by_token
from pokeapi.presentation.schemas.user import (
    User,
    UserCreationResult,
    UserErrors,
    UserInput,
)
from tests.conftest import TEST_TOKEN_ENTITY, TEST_USER_ENTITY, MockInfo


class TestUserGetResolver:
    def test_get_user_by_token(self, mock_access_info: MockInfo) -> None:
        container = mock_access_info.context["container"]
        service = container.get(UserService)
        service.get_by_token = MagicMock(return_value=TEST_USER_ENTITY)
        actual = get_user_by_token(mock_access_info)  # type: ignore

        assert isinstance(actual, User)
        assert actual.username == "Red"

    def test_get_user_by_token_header_error(self, mock_info: MockInfo) -> None:
        actual = get_user_by_token(mock_info)  # type: ignore

        assert isinstance(actual, UserErrors)
        assert actual.message == "User is unauthorized."

    def test_get_user_by_token_error(self, mock_access_info: MockInfo) -> None:
        container = mock_access_info.context["container"]
        service = container.get(UserService)
        service.get_by_token = MagicMock(side_effect=TokenVerificationError("error"))
        actual = get_user_by_token(mock_access_info)  # type: ignore

        assert isinstance(actual, UserErrors)
        assert actual.message == "error"


class TestUserCreationResolver:
    def test_create_user(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(UserService)
        service._password_service.hash = MagicMock(return_value="hashed_password")  # type: ignore
        service._token_service.create = MagicMock(return_value=TEST_TOKEN_ENTITY)  # type: ignore
        actual = create_user(
            UserInput(username="mock", password="password"),
            mock_info,  # type: ignore
        )

        assert isinstance(actual, UserCreationResult)
        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"

    def test_create_user_error(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(UserService)
        service.create = MagicMock(side_effect=UserCreationError("error"))
        actual = create_user(
            UserInput(username="mock", password="password"),
            mock_info,  # type: ignore
        )

        assert isinstance(actual, UserErrors)
        assert actual.message == "error"
