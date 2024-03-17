from pokeapi.presentation.schemas.user import User, UserCreationResult, UserErrors
from tests.conftest import TEST_TOKEN_ENTITY, TEST_USER_ENTITY


class TestUserSchema:
    def test_from_entity(self) -> None:
        assert User.from_entity(TEST_USER_ENTITY) == User(username="Red")


class TestUserCreationResultSchema:
    def test_from_entity(self) -> None:
        assert UserCreationResult.from_entity(TEST_TOKEN_ENTITY) == UserCreationResult(
            access_token="access_token",
            refresh_token="refresh_token",
            token_type="Bearer",
        )


class TestUserErrorsSchema:
    def test_from_exception(self) -> None:
        assert UserErrors.from_exception(Exception("error")) == UserErrors(
            message="error"
        )
