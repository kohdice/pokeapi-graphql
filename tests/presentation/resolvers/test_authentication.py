from unittest.mock import MagicMock

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.exceptions.authentication import AuthenticationError
from pokeapi.presentation.resolvers.authentication import auth, refresh
from pokeapi.presentation.schemas.authentication import AuthErrors, AuthResult
from tests.conftest import TEST_TOKEN_ENTITY, TEST_USER_INPUT, MockInfo


class TestAuthResolver:
    def test_auth(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(AuthenticationService)
        service.auth = MagicMock(return_value=TEST_TOKEN_ENTITY)
        actual = auth(TEST_USER_INPUT, mock_info)  # type: ignore

        assert isinstance(actual, AuthResult)
        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"

    def test_auth_error(self, mock_info: MockInfo) -> None:
        container = mock_info.context["container"]
        service = container.get(AuthenticationService)
        service.auth = MagicMock(side_effect=AuthenticationError("error"))
        actual = auth(TEST_USER_INPUT, mock_info)  # type: ignore

        assert isinstance(actual, AuthErrors)
        assert actual.message == "error"


class TestRefreshResolver:
    def test_refresh(self, mock_refresh_info: MockInfo) -> None:
        container = mock_refresh_info.context["container"]
        service = container.get(AuthenticationService)
        service.refresh = MagicMock(return_value=TEST_TOKEN_ENTITY)
        actual = refresh(mock_refresh_info)  # type: ignore

        assert isinstance(actual, AuthResult)
        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"

    def test_refresh_auth_header_error(self, mock_info: MockInfo) -> None:
        actual = refresh(mock_info)  # type: ignore

        assert isinstance(actual, AuthErrors)
        assert actual.message == "User is unauthorized."

    def test_refresh_auth_error(self, mock_refresh_info: MockInfo) -> None:
        container = mock_refresh_info.context["container"]
        service = container.get(AuthenticationService)
        service.refresh = MagicMock(side_effect=AuthenticationError("error"))
        actual = refresh(mock_refresh_info)  # type: ignore

        assert isinstance(actual, AuthErrors)
        assert actual.message == "error"

    def test_refresh_user_not_found_error(self, mock_refresh_info: MockInfo) -> None:
        container = mock_refresh_info.context["container"]
        service = container.get(AuthenticationService)
        service.refresh = MagicMock(side_effect=AuthenticationError("error"))
        actual = refresh(mock_refresh_info)  # type: ignore

        assert isinstance(actual, AuthErrors)
        assert actual.message == "error"
