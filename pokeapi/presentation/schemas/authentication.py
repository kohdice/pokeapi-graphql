import strawberry

from pokeapi.domain.entities.token import Token


@strawberry.type(description="A schema representing an authentication result.")
class AuthResult:
    """A class representing an authentication result.

    This class represents an authentication result, which contains information
    about an access token, a refresh token and a token type.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The token type.

    """

    access_token: str = strawberry.field(description="The access token.")
    refresh_token: str = strawberry.field(description="The refresh token.")
    token_type: str = strawberry.field(description="The token type.")

    @classmethod
    def from_entity(cls, entity: Token) -> "AuthResult":
        """Create an authentication result schema from a token entity.

        Args:
            entity (Token): The token entity.

        Returns:
            AuthResult: The authentication result schema.

        """

        return cls(
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            token_type=entity.token_type,
        )


@strawberry.type(description="A schema representing an authentication error.")
class AuthErrors:
    """A class representing an authentication error.

    This class represents an authentication error,
    which contains information about an error message.

    Attributes:
        message (str): The error message.

    """

    message: str = strawberry.field(description="The error message.")

    @classmethod
    def from_exception(cls, exception: Exception) -> "AuthErrors":
        """Create an authentication error schema from an exception.

        Args:
            exception (Exception): The exception.

        Returns:
            AuthErrors: The authentication error schema.

        """
        return cls(message=str(exception))
