import datetime
from abc import ABC, abstractmethod

from pokeapi.domain.entities.user import User


class JWTServiceABC(ABC):
    """Abstract class for JWT token creation and decoding.

    This class is an abstract class that defines the methods that a JWT token
    creation and decoding service should implement.


    """

    @abstractmethod
    def create_token(self, entity: User, exp: datetime.datetime, jti: str) -> str:
        """Create a JWT token.

        Args:
            entity (User): The entity to be used as the payload.
            exp (datetime.datetime): The expiration date of the token.
            jti (str): The JWT ID.

        Returns:
            str: The JWT token.

        """
        pass  # pragma: no cover

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode a JWT token.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            dict: The decoded payload.

        """
        pass  # pragma: no cover
