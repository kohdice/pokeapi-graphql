import datetime
import logging

from injector import inject, singleton

from pokeapi.dependencies.settings.config import AppConfigABC
from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.user import User
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.domain.services.password_abc import PasswordServiceABC
from pokeapi.domain.services.token_abc import TokenServiceABC
from pokeapi.exceptions.authorization import AuthorizationError
from pokeapi.exceptions.user import UserNotFoundError

from .user_abc import UserServiceABC


@singleton
class UserService(UserServiceABC):
    """Concrete implementation of a user service.

    This class provides concrete implementations of the abstract methods defined in the
    UserServiceABC class. It is responsible for handling user creation and retrieval.

    Attributes:
        _logger (logging.Logger): The logger for this class.
        _config (AppConfigABC): The application configuration.
        _password_service (PasswordServiceABC): The service used to hash and verify passwords.
        _token_service (TokenServiceABC): The service used to generate and verify tokens.
        _token_whitelist_repo (TokenWhitelistRepositoryABC):
            The repository used to manage token whitelists.
        _user_repo (UserRepositoryABC): The repository used to retrieve user data.

    """

    @inject
    def __init__(
        self,
        config: AppConfigABC,
        password_service: PasswordServiceABC,
        token_service: TokenServiceABC,
        token_whitelist_repo: TokenWhitelistRepositoryABC,
        user_repo: UserRepositoryABC,
    ) -> None:
        """Initialize the UserService with services and repositories.

        Args:
            config (AppConfigABC): The application configuration.
            password_service (PasswordServiceABC): The service used to hash and verify passwords.
            token_service (TokenServiceABC): The service used to generate and verify tokens.
            token_whitelist_repo (TokenWhitelistRepositoryABC):
                The repository used to manage token whitelists.
            user_repo (UserRepositoryABC): The repository used to retrieve user data.

        """
        self._logger = logging.getLogger(__name__)
        self._config = config
        self._password_service = password_service
        self._token_service = token_service
        self._token_whitelist_repo = token_whitelist_repo
        self._user_repo = user_repo

    def get_by_token(self, token: str) -> User:
        payload = self._token_service.extract_payload(token)
        exp = datetime.datetime.now() - datetime.timedelta(
            hours=self._config.access_token_lifetime
        )
        valid_token = self._token_whitelist_repo.get_by_access_token(
            payload["jti"], exp
        )

        if not valid_token:
            self._logger.info(
                "The token was not found in the whitelist with the specified access token."
            )
            raise AuthorizationError("User is unauthorized")

        user = self._user_repo.get_by_id(payload["sub"])

        if user is None:
            self._logger.info(
                "The user associated with the specified access token was not found."
                f"user_id: {payload['sub']}"
            )
            raise UserNotFoundError("User not found")

        # NOTE: Delete expired tokens.
        refresh_exp = datetime.datetime.now() - datetime.timedelta(
            hours=self._config.refresh_token_lifetime
        )
        self._token_whitelist_repo.delete(user.id_, refresh_exp)

        return user

    def create(self, username: str, password: str) -> Token:
        """Create a new user and return a token.

        This method creates a new user with the given username and password and returns a token for
        the new user.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            Token: The token issued to the new user.

        """
        user = User(username=username, password=self._password_service.hash(password))

        created_user = self._user_repo.create(user)

        return self._token_service.create(created_user)
