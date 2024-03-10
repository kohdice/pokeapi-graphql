import pytest
from injector import Injector
from pytest_mock import MockerFixture

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.exceptions.authentication import AuthenticationError
from pokeapi.exceptions.user import UserNotFoundError


@pytest.fixture(scope="module")
def service(container: Injector) -> AuthenticationService:
    return container.get(AuthenticationService)


class TestAuthenticationService:
    def test_auth(self, service: AuthenticationService, mocker: MockerFixture) -> None:
        mocker.patch("uuid.uuid4", return_value="refresh")
        actual = service.auth("mock_user", "password")

        assert actual.access_token == "token"
        assert actual.refresh_token == "refresh"
        assert actual.token_type == "Bearer"

    def test_auth_user_not_found(self, service: AuthenticationService) -> None:
        with pytest.raises(AuthenticationError):
            service.auth("not_found", "password")

    def test_auth_invalid_password(self, service: AuthenticationService) -> None:
        with pytest.raises(AuthenticationError):
            service.auth("mock_user", "invalid_password")

    def test_refresh(
        self, service: AuthenticationService, mocker: MockerFixture
    ) -> None:
        mocker.patch("uuid.uuid4", return_value="refresh")
        actual = service.refresh("refresh_token")

        assert actual.access_token == "token"
        assert actual.refresh_token == "refresh"
        assert actual.token_type == "Bearer"

    def test_refresh_token_not_found(self, service: AuthenticationService) -> None:
        with pytest.raises(AuthenticationError):
            service.refresh("invalid_refresh_token")

    def test_refresh_user_not_found(self, service: AuthenticationService) -> None:
        with pytest.raises(UserNotFoundError):
            service.refresh("no_user_refresh_token")

    def test_create_user(
        self, service: AuthenticationService, mocker: MockerFixture
    ) -> None:
        mocker.patch("uuid.uuid4", return_value="refresh")
        actual = service.create_user("mock_user", "password")

        assert actual.access_token == "token"
        assert actual.refresh_token == "refresh"
        assert actual.token_type == "Bearer"
