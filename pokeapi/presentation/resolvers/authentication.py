from strawberry.types.info import Info

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.exceptions.authentication import AuthenticationError
from pokeapi.exceptions.user import UserCreationError, UserNotFoundError
from pokeapi.presentation.schemas.authentication import AuthErrors, AuthResult
from pokeapi.presentation.schemas.user import UserInput


def auth(input: UserInput, info: Info) -> AuthResult | AuthErrors:  # noqa A002
    """Authenticates a user and returns a token.

    Args:
        input (UserInput): The input data.
        info (Info): The query info.

    Returns:
        AuthResult | AuthErrors: The token or an error message.

    """
    validated_input = input.to_pydantic()
    container = info.context.get("container")
    service = container.get(AuthenticationService)

    try:
        token = service.auth(validated_input.username, validated_input.password)
    except AuthenticationError as e:
        return AuthErrors(message=str(e))

    return AuthResult(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
    )


def refresh(token: str, info: Info) -> AuthResult | AuthErrors:  # noqa A002
    """Refreshes a token.

    Args:
        token (str): The refresh token.
        info (Info): The query info.

    Returns:
        AuthResult | AuthErrors: The token or an error message.

    """
    container = info.context.get("container")
    service = container.get(AuthenticationService)

    try:
        refreshed_token = service.refresh(token)
    except (AuthenticationError, UserNotFoundError) as e:
        return AuthErrors(message=str(e))

    return AuthResult(
        access_token=refreshed_token.access_token,
        refresh_token=refreshed_token.refresh_token,
        token_type=refreshed_token.token_type,
    )


def user_create(input: UserInput, info: Info) -> AuthResult | AuthErrors:  # noqa A002
    """Creates a new user and returns a token.

    Args:
        input (UserInput): The input data.
        info (Info): The query info.

    Returns:
        AuthResult | AuthErrors: The token or an error message.

    """
    validated_input = input.to_pydantic()
    container = info.context.get("container")
    service = container.get(AuthenticationService)

    try:
        token = service.create_user(validated_input.username, validated_input.password)
    except UserCreationError as e:
        return AuthErrors(message=str(e))

    return AuthResult(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
    )
