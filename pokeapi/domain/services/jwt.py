import datetime
import logging

from injector import inject, singleton
from jose import JWTError, jwt

from pokeapi.dependencies.settings.config import AppConfigABC
from pokeapi.domain.entities.user import User
from pokeapi.exceptions.token import TokenVerificationError

from .jwt_abc import JWTServiceABC


@singleton
class JWTService(JWTServiceABC):
    """Service for JWT token creation and decoding.

    This class provides the methods for creating and decoding JWT tokens.

    Attributes:
        _config (AppConfigABC): The application configuration.
        _logger (logging.Logger): The logger instance.

    """

    @inject
    def __init__(self, config: AppConfigABC) -> None:
        """Initialize the TokenServices class.

        Args:
            config (AppConfigABC): The application configuration.

        """
        self._config = config
        self._logger = logging.getLogger(__name__)

    def create_token(self, entity: User, exp: datetime.datetime, jti: str) -> str:  # type: ignore
        """Create a JWT token.

        Args:
            entity (User): The user entity.

        Returns:
            str: The JWT token.

        Raises:
            TypeError: If the token is not a string.

        """
        data = {
            "iss": self._config.app_domain,
            "sub": str(entity.id_),
            "exp": exp.timestamp(),
            "iat": datetime.datetime.now().timestamp(),
            "jti": jti,
            "username": entity.username,
        }

        token = jwt.encode(
            data, self._config.private_key, algorithm=self._config.jwt_algorithm
        )

        # NOTE: The token is a string, but the type hint is not recognized.
        if not isinstance(token, str):
            raise TypeError("The token is not a string.")

        return token

    def decode_token(self, token: str) -> dict:
        """Decode a JWT token.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            dict: The decoded payload.

        Raises:
            TokenVerificationError: If the token is invalid.
            TypeError: If the payload is not a dictionary.

        """
        try:
            payload = jwt.decode(
                token,
                self._config.public_key,
                algorithms=self._config.jwt_algorithm,
                issuer=self._config.app_domain,
            )
        except JWTError as e:
            self._logger.error(
                TokenVerificationError(f"Token verification failed: {e}")
            )
            raise TokenVerificationError("Token verification failed.") from None

        # NOTE: The payload is a dict, but the type hint is not recognized.
        if not isinstance(payload, dict):
            raise TypeError("The payload is not a dictionary.")

        return payload
