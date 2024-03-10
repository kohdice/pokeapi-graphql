from .base import BaseEntity


class Token(BaseEntity):
    """A token entity.

    This class represents a token entity, which contains information about an access token
    and a refresh token.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The token type.

    """

    access_token: str
    refresh_token: str
    token_type: str
