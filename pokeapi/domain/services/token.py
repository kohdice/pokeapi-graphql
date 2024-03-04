import datetime
import logging

from injector import inject, singleton
from jose import JWTError, jwt

from pokeapi.dependencies.settings.config import AppConfigABC
from pokeapi.domain.entities.user import User
from pokeapi.exceptions.token import TokenVerificationError

from .token_abc import TokenServiceABC


@singleton
class TokenService(TokenServiceABC):
    """Token services.

    token services to create and decode JWT tokens.

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

        """
        data = {
            "iss": self._config.app_domain,
            "sub": str(entity.id_),
            "exp": exp.timestamp(),
            "iat": datetime.datetime.utcnow().timestamp(),
            "jti": jti,
            "username": entity.username,
        }

        token = jwt.encode(
            data, self._config.private_key, algorithm=self._config.jwt_algorithm
        )

        # NOTE: The token is a string, but the type hint is not recognized.
        assert isinstance(token, str)

        return token

    def decode_token(self, token: str) -> dict:
        """Decode a JWT token.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            dict: The decoded payload.

        Raises:
            TokenVerificationError: If the token is invalid.

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
        assert isinstance(payload, dict)

        if "jti" not in payload:
            self._logger.error(
                TokenVerificationError(
                    "Token verification failed: The token is invalid as it lacks the 'jti' claim."
                )
            )
            raise TokenVerificationError("Token verification failed.")

        return payload
