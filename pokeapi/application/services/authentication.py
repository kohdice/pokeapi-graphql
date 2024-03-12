import datetime
import logging

from injector import inject, singleton

from pokeapi.dependencies.settings.config import AppConfigABC
from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.token_whitelist import TokenWhitelist
from pokeapi.domain.entities.user import User
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.domain.services.password_abc import PasswordServiceABC
from pokeapi.domain.services.token_abc import TokenServiceABC
from pokeapi.exceptions.authentication import AuthenticationError
from pokeapi.exceptions.user import UserNotFoundError

from .authentication_abc import AuthenticationServiceABC


@singleton
class AuthenticationService(AuthenticationServiceABC):
    """Concrete implementation of an authentication service.

    This class provides concrete implementations of the abstract methods defined in the
    AuthenticationServiceABC class. It is responsible for handling user authentication.

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
        """Initialize the AuthenticationService with services and repositories.

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

    def auth(self, username: str, password: str) -> Token:
        """Authenticate a user and return a token.

        This method authenticates a user with the given credentials and returns a token if the
        credentials are valid. If the user is not found or the password is incorrect, an
        AuthenticationError is raised.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            Token: The token issued to the user.

        Raises:
            AuthenticationError: If the user is not found or the password is incorrect.

        """
        user: User | None = self._user_repo.get_by_username(username)

        if user is None:
            self._logger.info(
                AuthenticationError(f"User not found. username: {username}")
            )
            raise AuthenticationError(f"User not found. username: {username}")

        if not self._password_service.verify(password, user.password):
            self._logger.info(
                AuthenticationError(f"Invalid password. user_id: {user.id_}")
            )
            raise AuthenticationError("Password is incorrect.")

        # NOTE: Delete expired tokens.
        exp = datetime.datetime.now() - datetime.timedelta(
            hours=self._config.refresh_token_lifetime
        )
        self._token_whitelist_repo.delete(user.id_, exp)

        return self._token_service.create(user)

    def refresh(self, token: str) -> Token:
        """Refresh a user's token.

        This method refreshes a user's token using the refresh token provided. If the refresh token
        is not found or has expired, an AuthenticationError is raised. If the user associated with
        the refresh token is not found, a UserNotFoundError is raised.

        Args:
            token (str): The refresh token to use to refresh the user's token.

        Returns:
            Token: The refreshed token.

        Raises:
            AuthenticationError: If the refresh token is not found or has expired.
            UserNotFoundError: If the user associated with the refresh token is not found.

        """
        exp = datetime.datetime.now() - datetime.timedelta(
            hours=self._config.refresh_token_lifetime
        )
        valid_token: TokenWhitelist | None = (
            self._token_whitelist_repo.get_by_refresh_token(token, exp)  # type: ignore
        )

        if valid_token is None:
            self._logger.info(
                "The token was not found in the whitelist with the specified refresh token."
            )
            raise AuthenticationError("User is not authenticated.")

        user: User | None = self._user_repo.get_by_id(valid_token.user_id)

        if user is None:
            self._logger.info(
                ValueError(
                    "The user associated with the specified refresh token was not found."
                )
            )
            raise UserNotFoundError("User not found.")

        # NOTE: Delete expired tokens.
        exp = datetime.datetime.now() - datetime.timedelta(
            hours=self._config.refresh_token_lifetime
        )
        self._token_whitelist_repo.delete(user.id_, exp)

        return self._token_service.update(user, valid_token.id_)

    def create_user(self, username: str, password: str) -> Token:
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
