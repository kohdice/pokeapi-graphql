import datetime

from injector import inject, singleton

from pokeapi.domain.entities.token_whitelist import (
    TokenWhitelist as TokenWhitelistEntity,
)
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.infrastructure.database.models.token_whitelist import (
    TokenWhitelist as TokenWhitelistModel,
)


@singleton
class MockTokenWhitelistRepository(TokenWhitelistRepositoryABC):
    @inject
    def __init__(self) -> None:
        self.__now = datetime.datetime.now()
        self.__token = TokenWhitelistEntity(
            id_=1,
            user_id=1,
            access_token="foo",
            refresh_token="bar",
            created_by="mock_user",
            created_at=self.__now,
            updated_by="mock_user",
            updated_at=self.__now,
        )

    def _convert_to_entity(self, model: TokenWhitelistModel) -> TokenWhitelistEntity:  # type: ignore[override]
        return self.__token

    def get_by_access_token(  # type: ignore[override]
        self, entity: TokenWhitelistEntity, expiration: datetime.datetime
    ) -> TokenWhitelistEntity | None:
        if entity.access_token == "foo":
            return self.__token

        return None

    def get_by_refresh_token(  # type: ignore[override]
        self, entity: TokenWhitelistEntity, expiration: datetime.datetime
    ) -> TokenWhitelistEntity | None:
        if entity.refresh_token == "bar":
            return self.__token

        return None

    def create(self, entity: TokenWhitelistEntity) -> None:  # type: ignore[override]
        pass

    def update(self, entity: TokenWhitelistEntity) -> None:  # type: ignore[override]
        pass

    def delete(self, user_id: int, expiration: datetime.datetime) -> None:
        pass