import datetime
from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity


class TokenServiceABC(ABC):
    """Abstract class for Token services.

    This class is used to define the methods that will be used to create and decode JWT tokens.

    """

    @abstractmethod
    def create_token(self, entity: BaseEntity, exp: datetime.datetime, jti: str) -> str:
        """Create a JWT token.

        Args:
            entity (BaseEntity): The entity to be used as the payload.
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
