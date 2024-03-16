import pytest

from pokeapi.exceptions.authorization import AuthorizationError
from pokeapi.presentation.helpers.request_utils import extract_bearer_token
from tests.conftest import TEST_UUID, MockRequest


def test_extract_bearer_token(mock_refresh_request: MockRequest) -> None:
    actual = extract_bearer_token(mock_refresh_request)  # type: ignore

    assert actual == TEST_UUID


def test_extract_bearer_token_no_auth_header() -> None:
    with pytest.raises(AuthorizationError):
        extract_bearer_token(MockRequest())  # type: ignore


@pytest.mark.parametrize(
    "token", ["Bearer", "Bearer test_bearer_token hoge", "hogehoge"]
)
def test_extract_bearer_token_invalid_auth_header(token: str) -> None:
    with pytest.raises(AuthorizationError):
        extract_bearer_token(
            MockRequest(headers={"Authorization": token})  # type: ignore
        )
