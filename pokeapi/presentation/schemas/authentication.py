import strawberry


@strawberry.type
class AuthResult:
    """A class representing an authentication result.

    This class represents an authentication result, which contains information
    about an access token, a refresh token and a token type.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The token type.

    """

    access_token: str
    refresh_token: str
    token_type: str


@strawberry.type
class AuthErrors:
    """A class representing an authentication error.

    This class represents an authentication error,
    which contains information about an error message.

    Attributes:
        message (str): The error message.

    """

    message: str
