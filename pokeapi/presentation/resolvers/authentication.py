from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.types.info import Info

from pokeapi.application.services.authentication import AuthenticationService
from pokeapi.exceptions.authentication import AuthenticationError
from pokeapi.exceptions.authorization import AuthorizationError
from pokeapi.exceptions.user import UserNotFoundError
from pokeapi.presentation.helpers.request_utils import extract_bearer_token
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


def refresh(info: Info) -> AuthResult | AuthErrors:  # noqa A002
    """Refreshes a token.

    Args:
        info (Info): The query info.

    Returns:
        AuthResult | AuthErrors: The token or an error message.

    """
    request: Request | WebSocket = info.context["request"]
    container = info.context.get("container")
    service = container.get(AuthenticationService)

    try:
        token = extract_bearer_token(request)
    except AuthorizationError as e:
        return AuthErrors(message=str(e))

    try:
        refreshed_token = service.refresh(token)
    except (AuthenticationError, UserNotFoundError) as e:
        return AuthErrors(message=str(e))

    return AuthResult(
        access_token=refreshed_token.access_token,
        refresh_token=refreshed_token.refresh_token,
        token_type=refreshed_token.token_type,
    )
