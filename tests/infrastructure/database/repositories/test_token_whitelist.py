import datetime
from collections.abc import Generator

import pytest
from freezegun import freeze_time
from injector import Injector
from sqlalchemy import and_, delete, insert, select
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

ISSUANCE_DATE = datetime.datetime(2000, 1, 1, 1, 0, 0)
EXECUTION_DATE = datetime.datetime(2000, 1, 1, 1, 10, 0)


@pytest.fixture(scope="module")
def repo(dependency_container: Injector) -> TokenWhitelistRepository:
    session = dependency_container.get(Session)

    return TokenWhitelistRepository(session)


@pytest.fixture(scope="module")
def setup_user(dependency_container: Injector) -> Generator:
    session = dependency_container.get(Session)
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
def setup_token(
    dependency_container: Injector,
    setup_user: int,
) -> Generator:
    session = dependency_container.get(Session)
    record = session.execute(
        insert(TokenWhitelistModel).values(
            user_id=setup_user,
            access_token="foo",
            refresh_token="bar",
            created_by="test_repository",
            created_at=ISSUANCE_DATE,
            updated_by="test_repository",
            updated_at=ISSUANCE_DATE,
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
def _create_teardown(dependency_container: Injector, setup_user: int) -> Generator:
    yield

    session = dependency_container.get(Session)
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
                created_at=ISSUANCE_DATE,
                updated_by="test_repository",
                updated_at=ISSUANCE_DATE,
            )
        )
        assert isinstance(actual, TokenWhitelistEntity)
        assert actual.id_ == 1
        assert actual.user_id == 1
        assert actual.access_token == "foo"
        assert actual.refresh_token == "bar"

    @pytest.mark.usefixtures("setup_token")
    @freeze_time(EXECUTION_DATE)
    def test_get_by_access_token(
        self, repo: TokenWhitelistRepository, setup_user: int
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_access_token(
            TokenWhitelistEntity(
                id_=None,
                user_id=setup_user,
                access_token="foo",
                refresh_token=None,
                created_by="test_repository",
                created_at=None,
                updated_by="test_repository",
                updated_at=None,
            ),
            expiration,
        )

        assert isinstance(actual, TokenWhitelistEntity)
        assert actual.user_id == setup_user
        assert actual.access_token == "foo"

    def test_get_by_access_token_not_found(
        self, repo: TokenWhitelistRepository
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_access_token(
            TokenWhitelistEntity(
                id_=None,
                user_id=0,
                access_token="foo",
                refresh_token=None,
                created_by="test_repository",
                created_at=None,
                updated_by="test_repository",
                updated_at=None,
            ),
            expiration,
        )

        assert actual is None

    @pytest.mark.usefixtures("setup_token")
    @freeze_time(EXECUTION_DATE)
    def test_get_by_refresh_token(
        self, repo: TokenWhitelistRepository, setup_user: int
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_refresh_token(
            TokenWhitelistEntity(
                id_=None,
                user_id=setup_user,
                access_token=None,
                refresh_token="bar",
                created_by="test_repository",
                created_at=None,
                updated_by="test_repository",
                updated_at=None,
            ),
            expiration,
        )

        assert isinstance(actual, TokenWhitelistEntity)
        assert actual.user_id == setup_user
        assert actual.refresh_token == "bar"

    def test_get_by_refresh_token_not_found(
        self, repo: TokenWhitelistRepository
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        actual = repo.get_by_refresh_token(
            TokenWhitelistEntity(
                id_=None,
                user_id=0,
                access_token=None,
                refresh_token="bar",
                created_by="test_repository",
                created_at=None,
                updated_by="test_repository",
                updated_at=None,
            ),
            expiration,
        )

        assert actual is None

    @pytest.mark.usefixtures("_create_teardown")
    @freeze_time(ISSUANCE_DATE)
    def test_create(
        self,
        dependency_container: Injector,
        repo: TokenWhitelistRepository,
        setup_user: int,
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=None,
            user_id=setup_user,
            access_token="foo",
            refresh_token="bar",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )

        repo.create(entity)

        session = dependency_container.get(Session)
        actual = session.execute(
            select(TokenWhitelistModel).where(TokenWhitelistModel.user_id == setup_user)
        ).scalar()

        assert actual is not None
        assert actual.user_id == setup_user
        assert actual.access_token == "foo"
        assert actual.refresh_token == "bar"

    def test_create_with_error(
        self,
        repo: TokenWhitelistRepository,
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=None,
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
        dependency_container: Injector,
        repo: TokenWhitelistRepository,
        setup_user: int,
        setup_token: int,
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=setup_token,
            user_id=setup_user,
            access_token="baz",
            refresh_token="qux",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )
        repo.update(entity)

        session = dependency_container.get(Session)
        actual = session.execute(
            select(TokenWhitelistModel).where(TokenWhitelistModel.id_ == setup_token)
        ).scalar()

        assert actual is not None
        assert actual.user_id == setup_user
        assert actual.access_token == "baz"
        assert actual.refresh_token == "qux"

    def test_update_with_error(
        self, repo: TokenWhitelistRepository, setup_user: int
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=0,
            user_id=setup_user,
            access_token="baz",
            refresh_token="qux",
            created_by="test_repository",
            created_at=datetime.datetime.now(),
            updated_by="test_repository",
            updated_at=datetime.datetime.now(),
        )
        with pytest.raises(TokenUpdateError):
            repo.update(entity)

    def test_update_with_user_error(
        self, repo: TokenWhitelistRepository, setup_token: int
    ) -> None:
        entity = TokenWhitelistEntity(
            id_=setup_token,
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

    @pytest.mark.usefixtures("setup_token")
    @freeze_time("2999-01-01 01:00:00")
    def test_delete(
        self,
        dependency_container: Injector,
        repo: TokenWhitelistRepository,
        setup_user: int,
    ) -> None:
        expiration = datetime.datetime.now() - datetime.timedelta(hours=1)
        repo.delete(setup_user, expiration)

        session = dependency_container.get(Session)
        actual = session.execute(
            select(TokenWhitelistModel).where(
                and_(
                    TokenWhitelistModel.user_id == setup_user,
                    TokenWhitelistModel.deleted_at.isnot(None),
                )
            )
        ).all()

        assert len(actual) == 1
