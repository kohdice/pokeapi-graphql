from injector import inject, singleton

from pokeapi.domain.entities.user import User as UserEntity
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.infrastructure.database.models.users import User as UserModel


@singleton
class MockUserRepository(UserRepositoryABC):
    @inject
    def __init__(self) -> None:
        self.__user = UserEntity(id_=1, username="mock_user", password="")

    def _convert_to_entity(self, model: UserModel) -> UserEntity:
        return self.__user

    def get_by_id(self, id_: int) -> UserEntity | None:
        if id_ > 0:
            return self.__user

        return None

    def get_by_username(self, username: str) -> UserEntity | None:
        if username == "mock_user":
            return self.__user

        return None

    def create(self, entity: UserEntity) -> UserEntity:
        return self.__user

    def update(self, entity: UserEntity) -> UserEntity:
        return self.__user
