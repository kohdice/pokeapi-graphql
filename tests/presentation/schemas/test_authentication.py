from pokeapi.presentation.schemas.authentication import AuthErrors, AuthResult
from tests.conftest import TEST_TOKEN_ENTITY


class TestAuthResultSchema:
    def test_from_entity(self) -> None:
        assert AuthResult.from_entity(TEST_TOKEN_ENTITY) == AuthResult(
            access_token="access_token",
            refresh_token="refresh_token",
            token_type="Bearer",
        )


class TestAuthErrorsSchema:
    def test_from_exception(self) -> None:
        assert AuthErrors.from_exception(Exception("error")) == AuthErrors(
            message="error"
        )
