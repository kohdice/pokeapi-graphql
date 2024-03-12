import datetime
import uuid

from injector import inject, singleton

from pokeapi.dependencies.settings.config_abc import AppConfigABC
from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.token_whitelist import TokenWhitelist
from pokeapi.domain.entities.user import User
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.domain.services.jwt_abc import JWTServiceABC

from .token_abc import TokenServiceABC


@singleton
class TokenService(TokenServiceABC):
    """Concrete implementation of a token service.

    This class provides concrete implementations of the abstract methods defined in the
    TokenServiceABC class. It is responsible for handling token creation and management.

    Attributes:
        _config (AppConfigABC): The application configuration.
        _jwt_service (JWTServiceABC):
            The service used to generate and verify tokens.
        _whitelist_repo (TokenWhitelistRepositoryABC):
            The repository used to manage token whitelists.

    """

    @inject
    def __init__(
        self,
        config: AppConfigABC,
        jwt_service: JWTServiceABC,
        whitelist_repo: TokenWhitelistRepositoryABC,
    ):
        """Initialize the TokenService with services and repositories.

        Args:
            config (AppConfigABC): The application configuration.
            jwt_service (JWTServiceABC):
                The service used to generate and verify tokens.
            whitelist_repo (TokenWhitelistRepositoryABC):
                The repository used to manage token whitelists.

        """
        self._config = config
        self._jwt_service = jwt_service
        self._whitelist_repo = whitelist_repo

    def create(self, entity: User) -> Token:
        """Create a new token for a user.

        This method creates a new token for the given user
        and stores it in the token whitelist.

        Args:
            entity (User): The user for whom to create a token.

        Returns:
            Token: The created token.

        """
        jti = str(uuid.uuid4())
        exp = datetime.datetime.utcnow() + datetime.timedelta(
            hours=self._config.access_token_lifetime
        )
        access_token = self._jwt_service.create_token(entity, exp, jti)
        refresh_token = str(uuid.uuid4())

        self._whitelist_repo.create(
            entity=TokenWhitelist(
                id_=None,
                user_id=entity.id_,
                access_token=jti,
                refresh_token=refresh_token,
                created_by=entity.username,
                created_at=datetime.datetime.now(),
                updated_by=entity.username,
                updated_at=datetime.datetime.now(),
            ),
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    def update(self, entity: User, whitelist_id: int) -> Token:
        """Update a token for a user.

        This method updates the token for the given user
        and stores it in the token whitelist.

        Args:
            entity (User): The user for whom to update the token.
            whitelist_id (int): The ID of the token whitelist entry.

        Returns:
            Token: The updated token.

        """
        jti = str(uuid.uuid4())
        exp = datetime.datetime.utcnow() + datetime.timedelta(
            hours=self._config.access_token_lifetime
        )
        access_token = self._jwt_service.create_token(entity, exp, jti)
        refresh_token = str(uuid.uuid4())

        self._whitelist_repo.create(
            entity=TokenWhitelist(
                id_=whitelist_id,
                user_id=entity.id_,
                access_token=jti,
                refresh_token=refresh_token,
                created_by=entity.username,
                created_at=datetime.datetime.now(),
                updated_by=entity.username,
                updated_at=datetime.datetime.now(),
            ),
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    def delete(self, entity: User) -> None:
        """Delete a token for a user.

        This method deletes the token for the given user
        from the token whitelist.

        Args:
            entity (User): The user for whom to delete the token.

        """
        token_exp = datetime.datetime.now() - datetime.timedelta(
            hours=self._config.refresh_token_lifetime
        )
        self._whitelist_repo.delete(entity.id_, token_exp)
