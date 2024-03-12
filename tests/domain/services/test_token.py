from unittest.mock import MagicMock

import pytest
from injector import Injector
from pytest_mock import MockerFixture

from pokeapi.domain.services.token import TokenService
from tests.conftest import TEST_USER_ENTITY


@pytest.fixture(scope="module")
def service(container: Injector) -> TokenService:
    return container.get(TokenService)


class TestTokenService:
    def test_create(self, service: TokenService, mocker: MockerFixture) -> None:
        mocker.patch("uuid.uuid4", return_value="test_uuid")
        service._jwt_service.create_token = MagicMock(return_value="test_token")  # type: ignore
        actual = service.create(TEST_USER_ENTITY)

        assert actual.access_token == "test_token"
        assert actual.refresh_token == "test_uuid"
        assert actual.token_type == "Bearer"

    def test_update(self, service: TokenService, mocker: MockerFixture) -> None:
        mocker.patch("uuid.uuid4", return_value="test_uuid")
        service._jwt_service.create_token = MagicMock(return_value="test_token")  # type: ignore

        actual = service.update(TEST_USER_ENTITY, 1)

        assert actual.access_token == "test_token"
        assert actual.refresh_token == "test_uuid"
        assert actual.token_type == "Bearer"

    def test_delete(self, service: TokenService) -> None:
        service.delete(TEST_USER_ENTITY)
