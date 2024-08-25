from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from injector import Injector
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from pokeapi.domain.entities.user import User as UserEntity
from pokeapi.exceptions.user import UserCreationError, UserUpdateError
from pokeapi.infrastructure.database.models import User as UserModel
from pokeapi.infrastructure.database.repositories.user import UserRepository


@pytest.fixture(scope="module")
def repo(container: Injector) -> UserRepository:
    return container.get(UserRepository)


@pytest.fixture
def mock_session() -> MagicMock:
    return MagicMock(spec=Session)


@pytest.fixture
def setup_for_user(container: Injector) -> Generator:
    session = container.get(Session)
    record = session.execute(
        insert(UserModel).values(
            username="test_repository",
            password="password",
            created_by="test_repository",
            updated_by="test_repository",
        )
    )
    assert record.inserted_primary_key is not None
    session.commit()

    yield record.inserted_primary_key[0]

    session.execute(
        delete(UserModel).where(UserModel.id_ == record.inserted_primary_key[0])
    )
    session.commit()


@pytest.fixture
def _teardown_for_create(container: Injector) -> Generator:
    yield

    session = container.get(Session)
    session.execute(delete(UserModel).where(UserModel.created_by == "test_repository"))
    session.commit()


class TestUserRepository:
    def test_convert_to_entity(self, repo: UserRepository) -> None:
        actual = repo._convert_to_entity(
            UserModel(id_=1, username="Red", password="password")
        )

        assert isinstance(actual, UserEntity)
        assert actual.id_ == 1
        assert actual.username == "Red"
        assert actual.password == "password"

    def test_get_by_id(self, repo: UserRepository) -> None:
        actual = repo.get_by_id(1)

        assert isinstance(actual, UserEntity)
        assert actual.username == "Red"

    def test_get_by_id_not_found(self, repo: UserRepository) -> None:
        assert repo.get_by_id(0) is None

    def test_get_by_username(self, repo: UserRepository) -> None:
        actual = repo.get_by_username("Red")

        assert isinstance(actual, UserEntity)
        assert actual.username == "Red"

    def test_get_by_username_not_found(self, repo: UserRepository) -> None:
        assert repo.get_by_username("hoge") is None

    @pytest.mark.usefixtures("_teardown_for_create")
    def test_create(self, repo: UserRepository) -> None:
        actual = repo.create(
            UserEntity(username="test_repository", password="password")
        )

        assert actual.username == "test_repository"
        assert actual.password == "password"

    def test_create_with_integrity_error(self, repo: UserRepository) -> None:
        with pytest.raises(UserCreationError):
            repo.create(UserEntity(username="Red", password="password"))

    def test_create_with_creation_error(self, mock_session: MagicMock) -> None:
        print(type(mock_session))
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.inserted_primary_key = None
        repo = UserRepository(mock_session)

        with pytest.raises(UserCreationError):
            repo.create(UserEntity(username="hoge", password="password"))

    def test_update(self, repo: UserRepository, setup_for_user: int) -> None:
        repo.update(
            UserEntity(id_=setup_for_user, username="Blue", password="password")
        )

        actual = repo.get_by_id(setup_for_user)

        assert isinstance(actual, UserEntity)
        assert actual.username == "Blue"

    def test_update_with_error(self, repo: UserRepository, setup_for_user: int) -> None:
        with pytest.raises(UserUpdateError):
            repo.update(
                UserEntity(id_=setup_for_user, username="Red", password="password")
            )

    def test_update_with_no_update(self, repo: UserRepository) -> None:
        with pytest.raises(UserUpdateError):
            repo.update(UserEntity(id_=0, username="no_update", password="password"))
