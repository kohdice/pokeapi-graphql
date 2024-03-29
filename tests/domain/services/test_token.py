from unittest.mock import MagicMock

import pytest
from injector import Injector
from pytest_mock import MockerFixture

from pokeapi.domain.services.token import TokenService
from pokeapi.exceptions.token import TokenVerificationError
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

    def test_extract_payload(self, service: TokenService) -> None:
        service._jwt_service.decode_token = MagicMock(  # type: ignore
            return_value={"sub": 1, "jti": "test_jti", "username": "test_user"}
        )
        actual = service.extract_payload("test_token")

        assert actual == {"sub": 1, "jti": "test_jti", "username": "test_user"}

    def test_extract_payload_invalid_sub(self, service: TokenService) -> None:
        service._jwt_service.decode_token = MagicMock(  # type: ignore
            return_value={"jti": "test_jti", "username": "test_user"}
        )
        with pytest.raises(TokenVerificationError):
            service.extract_payload("test_token")

    def test_extract_payload_invalid_jti(self, service: TokenService) -> None:
        service._jwt_service.decode_token = MagicMock(  # type: ignore
            return_value={"sub": 1, "username": "test_user"}
        )

        with pytest.raises(TokenVerificationError):
            service.extract_payload("test_token")

    def test_extract_payload_invalid_username(self, service: TokenService) -> None:
        service._jwt_service.decode_token = MagicMock(  # type: ignore
            return_value={"sub": 1, "jti": "test_jti"}
        )

        with pytest.raises(TokenVerificationError):
            service.extract_payload("test_token")
