from collections.abc import Generator

import pytest
from freezegun import freeze_time
from injector import Injector
from pytest_mock import MockerFixture
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session
from strawberry import Schema

from pokeapi.dependencies.context import get_context
from pokeapi.domain.services.jwt import JWTService
from pokeapi.infrastructure.database.models import TokenWhitelist, User
from pokeapi.presentation.schemas.mutation import Mutation
from pokeapi.presentation.schemas.query import Query
from tests.conftest import EXECUTION_DATETIME, ISSUE_DATETIME, TEST_UUID, MockRequest


@pytest.fixture()
def _setup_for_token(container: Injector) -> Generator:
    session = container.get(Session)
    record = session.execute(
        insert(TokenWhitelist).values(
            user_id=1,
            access_token=TEST_UUID,
            refresh_token=TEST_UUID,
            created_by="Red",
            created_at=ISSUE_DATETIME,
            updated_by="Red",
            updated_at=ISSUE_DATETIME,
        )
    )
    assert record.inserted_primary_key is not None
    session.commit()

    yield

    session.execute(
        delete(TokenWhitelist).where(
            TokenWhitelist.id_ == record.inserted_primary_key[0]
        )
    )
    session.commit()


@pytest.fixture()
def _teardown_for_token(container: Injector) -> Generator:
    yield

    session = container.get(Session)
    session.execute(delete(TokenWhitelist).where(TokenWhitelist.user_id == 1))
    session.commit()


@pytest.fixture()
def _teardown_for_create_user(container: Injector) -> Generator:
    yield

    session = container.get(Session)
    session.execute(
        delete(TokenWhitelist).where(TokenWhitelist.access_token == TEST_UUID)
    )
    session.execute(delete(User).where(User.username == "Green"))
    session.commit()


# TODO: Fix the test to support `strawberry.relay`.
@pytest.mark.skip(
    reason="When testing a Query class that uses strawberry.relay with Schema.execute_sync, it fails."
)
class TestMutation:
    @pytest.mark.usefixtures("_teardown_for_token")
    @freeze_time(ISSUE_DATETIME)
    def test_auth(self, access_token: str, mocker: MockerFixture) -> None:
        mocker.patch("uuid.uuid4", return_value=TEST_UUID)

        mutation = """
            mutation testAuth($input: UserInput!) {
                auth(input: $input) {
                    ... on AuthResult {
                        accessToken
                        refreshToken
                        tokenType
                    }
                    ... on AuthErrors {
                        message
                    }
                }
            }
        """
        schema = Schema(query=Query, mutation=Mutation)
        result = schema.execute_sync(
            mutation,
            variable_values={"input": {"username": "Red", "password": "password"}},
            context_value=get_context(),
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["auth"] == {
            "accessToken": access_token,
            "refreshToken": TEST_UUID,
            "tokenType": "Bearer",
        }

    @pytest.mark.usefixtures("_setup_for_token")
    @freeze_time(EXECUTION_DATETIME)
    def test_refresh(
        self,
        refreshed_access_token: str,
        mock_refresh_request: MockRequest,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch("uuid.uuid4", return_value=TEST_UUID)

        mutation = """
            mutation testRefresh {
                refresh {
                    ... on AuthResult {
                        accessToken
                        refreshToken
                        tokenType
                    }
                    ... on AuthErrors {
                        message
                    }
                }
            }
        """
        context = get_context()
        context["request"] = mock_refresh_request
        schema = Schema(query=Query, mutation=Mutation)
        result = schema.execute_sync(mutation, context_value=context)

        assert result.errors is None
        assert result.data is not None
        assert result.data["refresh"] == {
            "accessToken": refreshed_access_token,
            "refreshToken": TEST_UUID,
            "tokenType": "Bearer",
        }

    @pytest.mark.usefixtures("_teardown_for_create_user")
    def test_create_user(self, mocker: MockerFixture) -> None:
        mocker.patch("uuid.uuid4", return_value=TEST_UUID)
        mocker.patch.object(JWTService, "create_token", return_value="access_token")

        mutation = """
            mutation testCreateUser($input: UserInput!) {
                userCreate(input: $input) {
                    ... on AuthResult {
                        accessToken
                        refreshToken
                        tokenType
                    }
                    ... on AuthErrors {
                        message
                    }
                }
            }
        """
        schema = Schema(query=Query, mutation=Mutation)
        result = schema.execute_sync(
            mutation,
            variable_values={"input": {"username": "Green", "password": "password"}},
            context_value=get_context(),
        )

        assert result.errors is None
        assert result.data is not None
        assert result.data["userCreate"] == {
            "accessToken": "access_token",
            "refreshToken": TEST_UUID,
            "tokenType": "Bearer",
        }
