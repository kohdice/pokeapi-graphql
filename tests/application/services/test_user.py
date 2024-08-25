from unittest.mock import MagicMock

import pytest
from injector import Injector

from pokeapi.application.services.user import UserService
from pokeapi.exceptions.authorization import AuthorizationError
from pokeapi.exceptions.user import UserNotFoundError
from tests.conftest import (
    TEST_TOKEN_ENTITY,
    TEST_TOKEN_WHITELIST_ENTITY,
    TEST_USER_ENTITY,
)


@pytest.fixture
def service(container: Injector) -> UserService:
    return container.get(UserService)


class TestUserService:
    def test_get_by_token(self, service: UserService) -> None:
        service._token_service.extract_payload = MagicMock(  # type: ignore
            return_value={"sub": 1, "jti": "test_jti", "username": "Red"}
        )
        service._user_repo.get_by_id = MagicMock(return_value=TEST_USER_ENTITY)  # type: ignore

        service.get_by_token("token")

    def test_get_by_token_not_found_whitelist(self, service: UserService) -> None:
        service._token_service.extract_payload = MagicMock(  # type: ignore
            return_value={"sub": 1, "jti": "test_jti", "username": "Red"}
        )
        service._token_whitelist_repo.get_by_access_token = MagicMock(return_value=None)  # type: ignore

        with pytest.raises(AuthorizationError):
            service.get_by_token("not_found_token")

    def test_get_by_token_not_found_user(self, service: UserService) -> None:
        service._token_whitelist_repo.get_by_access_token = MagicMock(  # type: ignore
            return_value=TEST_TOKEN_WHITELIST_ENTITY
        )
        service._user_repo.get_by_id = MagicMock(return_value=None)  # type: ignore
        with pytest.raises(UserNotFoundError):
            service.get_by_token("not_found_token")

    def test_create(self, service: UserService) -> None:
        service._password_service.hash = MagicMock(return_value="hashed_password")  # type: ignore
        service._token_service.create = MagicMock(return_value=TEST_TOKEN_ENTITY)  # type: ignore
        actual = service.create("mock_user", "password")

        assert actual.access_token == "access_token"
        assert actual.refresh_token == "refresh_token"
        assert actual.token_type == "Bearer"
