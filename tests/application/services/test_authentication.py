from unittest.mock import MagicMock

import pytest
from injector import Injector

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.exceptions.authentication import AuthenticationError
from pokeapi.exceptions.user import UserNotFoundError
from tests.conftest import (
    TEST_TOKEN_ENTITY,
    TEST_TOKEN_WHITELIST_ENTITY,
    TEST_USER_ENTITY,
)


@pytest.fixture(scope="module")
def service(container: Injector) -> AuthenticationService:
    return container.get(AuthenticationService)


class TestAuthenticationService:
    def test_auth(self, service: AuthenticationService) -> None:
        service._token_service.create = MagicMock(return_value=TEST_TOKEN_ENTITY)  # type: ignore
        actual = service.auth("mock_user", "password")

        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"

    def test_auth_user_not_found(self, service: AuthenticationService) -> None:
        service._user_repo.get_by_username = MagicMock(return_value=None)  # type: ignore
        with pytest.raises(AuthenticationError):
            service.auth("not_found", "password")

    def test_auth_invalid_password(self, service: AuthenticationService) -> None:
        service._user_repo.get_by_username = MagicMock(return_value=TEST_USER_ENTITY)  # type: ignore
        service._password_service.verify = MagicMock(return_value=False)  # type: ignore
        with pytest.raises(AuthenticationError):
            service.auth("mock_user", "invalid_password")

    def test_refresh(self, service: AuthenticationService) -> None:
        service._token_service.update = MagicMock(return_value=TEST_TOKEN_ENTITY)  # type: ignore
        actual = service.refresh("token")

        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"

    def test_refresh_token_not_found(self, service: AuthenticationService) -> None:
        service._token_whitelist_repo.get_by_refresh_token = MagicMock(  # type: ignore
            return_value=None
        )
        with pytest.raises(AuthenticationError):
            service.refresh("invalid_refresh_token")

    def test_refresh_user_not_found(self, service: AuthenticationService) -> None:
        service._token_whitelist_repo.get_by_refresh_token = MagicMock(  # type: ignore
            return_value=TEST_TOKEN_WHITELIST_ENTITY
        )
        service._user_repo.get_by_id = MagicMock(return_value=None)  # type: ignore
        with pytest.raises(UserNotFoundError):
            service.refresh("no_user_refresh_token")

    def test_create_user(self, service: AuthenticationService) -> None:
        service._password_service.hash = MagicMock(return_value="hashed_password")  # type: ignore
        service._token_service.create = MagicMock(return_value=TEST_TOKEN_ENTITY)  # type: ignore
        actual = service.create_user("mock_user", "password")

        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"
