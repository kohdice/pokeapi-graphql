import datetime
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time
from injector import Injector
from pytest_mock import MockerFixture
from sqlalchemy import and_, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pokeapi.domain.entities.token_whitelist import (
    TokenWhitelist as TokenWhitelistEntity,
)
from pokeapi.exceptions.token import TokenRegistrationError, TokenUpdateError
from pokeapi.infrastructure.database.models.token_whitelist import (
    TokenWhitelist as TokenWhitelistModel,
)
from pokeapi.infrastructure.database.models.users import User
from pokeapi.infrastructure.database.repositories.token_whitelist import (
    TokenWhitelistRepository,
)
from tests.conftest import EXECUTION_DATETIME, ISSUE_DATETIME


@pytest.fixture(scope="module")
def repo(container: Injector) -> TokenWhitelistRepository:
    return container.get(TokenWhitelistRepository)


@pytest.fixture()
def mock_session() -> MagicMock:
    return MagicMock(spec=Session)


@pytest.fixture(scope="module")
def setup_user(container: Injector) -> Generator:
    session = container.get(Session)
    record = session.execute(
        insert(User).values(
            username="test_repository",
            password="password",
            created_by="test_repository",
            updated_by="test_repository",
        )
    )
    assert record.inserted_primary_key is not None
    session.commit()

    yield record.inserted_primary_key[0]

    session.execute(delete(User).where(User.id_ == record.inserted_primary_key[0]))
    session.commit()


@pytest.fixture()
def setup_token_whitelist(
    container: Injector,
    setup_user: int,
) -> Generator:
    session = container.get(Session)
    record = session.execute(
        insert(TokenWhitelistModel).values(
            user_id=setup_user,
            access_token="foo",
            refresh_token="bar",
            created_by="test_repository",
            created_at=ISSUE_DATETIME,
            updated_by="test_repository",
            updated_at=ISSUE_DATETIME,
        )
    )
    assert record.inserted_primary_key is not None
    session.commit()

    yield record.inserted_primary_key[0]

    session.execute(
        delete(TokenWhitelistModel).where(
            TokenWhitelistModel.id_ == record.inserted_primary_key[0]
        )
    )
    session.commit()


@pytest.fixture()
def _teardown_for_create(container: Injector, setup_user: int) -> Generator:
    yield

    session = container.get(Session)
    session.execute(
        delete(TokenWhitelistModel).where(TokenWhitelistModel.user_id == setup_user)
    )
    session.commit()


class TestTokenWhitelistRepository:
    def test_convert_to_entity(self, repo: TokenWhitelistRepository) -> None:
        actual = repo._convert_to_entity(
            TokenWhitelistModel(
                id_=1,
                user_id=1,
                access_token="foo",
                refresh_token="bar",
                created_by="test_repository",
                created_at=ISSUE_DATETIME,
                updated_by="test_repository",
                updated_at=ISSUE_DATETIME,
            )
        )
        assert isinstance(actual, TokenWhitelistEntity)
        assert actual.id_ == 1
        assert actual.user_id == 1
        assert actual.access_token == "foo"
        assert actual.refresh_token == "bar"

    @pytest.mark.usefixtures("setup_token_whitelist")
    @freeze_time(EXECUTION_DATETIME)
    def test_get_by_access_token(
        self, repo: TokenWhitelistRepository, setup_user: int
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_access_token("foo", expiration)

        assert isinstance(actual, TokenWhitelistEntity)
        assert actual.user_id == setup_user
        assert actual.access_token == "foo"

    def test_get_by_access_token_not_found(
        self, repo: TokenWhitelistRepository
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_access_token("hoge", expiration)

        assert actual is None

    @pytest.mark.usefixtures("setup_token_whitelist")
    @freeze_time(EXECUTION_DATETIME)
    def test_get_by_refresh_token(
        self, repo: TokenWhitelistRepository, setup_user: int
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_refresh_token("bar", expiration)

        assert isinstance(actual, TokenWhitelistEntity)
        assert actual.user_id == setup_user
        assert actual.refresh_token == "bar"

    def test_get_by_refresh_token_not_found(
        self, repo: TokenWhitelistRepository
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_refresh_token("bar", expiration)

        assert actual is None

    @pytest.mark.usefixtures("_teardown_for_create")
    @freeze_time(ISSUE_DATETIME)
    def test_create(
        self,
        repo: TokenWhitelistRepository,
        setup_user: int,
    ) -> None:
        entity = TokenWhitelistEntity(
            user_id=setup_user,
            access_token="foo",
            refresh_token="bar",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )

        actual = repo.create(entity)

        assert actual.user_id == setup_user
        assert actual.access_token == "foo"
        assert actual.refresh_token == "bar"

    def test_create_with_integrity_error(
        self,
        repo: TokenWhitelistRepository,
    ) -> None:
        entity = TokenWhitelistEntity(
            user_id=0,
            access_token="foo",
            refresh_token="bar",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )

        with pytest.raises(TokenRegistrationError):
            repo.create(entity)

    def test_create_with_creation_error(self, mock_session: MagicMock) -> None:
        print(type(mock_session))
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.inserted_primary_key = None
        repo = TokenWhitelistRepository(mock_session)
        entity = TokenWhitelistEntity(
            user_id=0,
            access_token="foo",
            refresh_token="bar",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )

        with pytest.raises(TokenRegistrationError):
            repo.create(entity)

    def test_update(
        self,
        container: Injector,
        repo: TokenWhitelistRepository,
        setup_user: int,
        setup_token_whitelist: int,
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=setup_token_whitelist,
            user_id=setup_user,
            access_token="baz",
            refresh_token="qux",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )
        repo.update(entity)

        session = container.get(Session)
        actual = session.execute(
            select(TokenWhitelistModel).where(
                TokenWhitelistModel.id_ == setup_token_whitelist
            )
        ).scalar()

        assert actual is not None
        assert actual.user_id == setup_user
        assert actual.access_token == "baz"
        assert actual.refresh_token == "qux"

    def test_update_integrity_error(
        self, repo: TokenWhitelistRepository, mocker: MockerFixture
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=0,
            user_id=0,
            access_token="baz",
            refresh_token="qux",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )
        mocker.patch.object(
            Session, "execute", side_effect=IntegrityError(None, None, Exception())
        )

        with pytest.raises(TokenUpdateError):
            repo.update(entity)

    def test_update_with_result_zero_error(self, mock_session: MagicMock) -> None:
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.rowcount = 0
        repo = TokenWhitelistRepository(mock_session)
        entity = TokenWhitelistEntity(
            id_=0,
            user_id=0,
            access_token="baz",
            refresh_token="qux",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )

        with pytest.raises(TokenUpdateError):
            repo.update(entity)

    @pytest.mark.usefixtures("setup_token_whitelist")
    @freeze_time("2999-01-01 01:00:00")
    def test_delete(
        self,
        container: Injector,
        repo: TokenWhitelistRepository,
        setup_user: int,
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        repo.delete(setup_user, expiration)

        session = container.get(Session)
        actual = session.execute(
            select(TokenWhitelistModel).where(
                and_(
                    TokenWhitelistModel.user_id == setup_user,
                    TokenWhitelistModel.deleted_at.isnot(None),
                )
            )
        ).all()

        assert len(actual) == 1
