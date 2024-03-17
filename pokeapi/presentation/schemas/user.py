import strawberry

from pokeapi.domain.entities.token import Token
from pokeapi.domain.entities.user import User as UserEntity
from pokeapi.presentation.validators.user import UserInputValidator


@strawberry.type(description="A schema representing a user.")
class User:
    """GraphQL schema for user.

    Attributes:
        username (str): The user's username

    """

    username: str = strawberry.field(description="The user's username")

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "User":
        """Create a user schema from a user entity.

        Args:
            entity (UserEntity): The user entity.

        Returns:
            User: The user schema.

        """
        return cls(username=entity.username)


@strawberry.experimental.pydantic.input(
    model=UserInputValidator, description="Input for the user."
)
class UserInput:
    """Input for the user

    Attributes:
        username (str): The username
        password (str): The password

    """

    username: str = strawberry.field(description="The username")
    password: str = strawberry.field(description="The password")


@strawberry.type(description="A schema representing a user creation.")
class UserCreationResult:
    """A class representing a user creation result.

    This class represents a user creation result, which contains information
    about the user and a token.

    Attributes:
        user (User): The user.
        token (AuthResult): The token.

    """

    access_token: str = strawberry.field(description="The access token.")
    refresh_token: str = strawberry.field(description="The refresh token.")
    token_type: str = strawberry.field(description="The token type.")

    @classmethod
    def from_entity(cls, entity: Token) -> "UserCreationResult":
        """Create a user creation result schema from a tokrn entity.

        Args:
            entity (Token): The token entity.

        Returns:
            UserCreationResult: The user creation result schema.

        """
        return cls(
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            token_type=entity.token_type,
        )


@strawberry.type(description="A schema representing a user error.")
class UserErrors:
    """A class representing a user error.

    This class represents a user error, which contains information
    about an error message.

    Attributes:
        message (str): The error message.

    """

    message: str = strawberry.field(description="The error message.")

    @classmethod
    def from_exception(cls, exception: Exception) -> "UserErrors":
        """Create a user error schema from an exception.

        Args:
            error (Exception): The exception.

        Returns:
            UserErrors: The user error schema.

        """
        return cls(message=str(exception))
