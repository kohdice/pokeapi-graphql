from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.types.info import Info

from pokeapi.application.services.user import UserService
from pokeapi.exceptions.authorization import AuthorizationError
from pokeapi.exceptions.token import TokenVerificationError
from pokeapi.exceptions.user import UserCreationError
from pokeapi.presentation.helpers.request_utils import extract_bearer_token
from pokeapi.presentation.schemas.user import (
    User,
    UserCreationResult,
    UserErrors,
    UserInput,
)


def get_user_by_token(info: Info) -> User | UserErrors:
    """Retrieves a user by token.

    Args:
        info (Info): The query info.

    Returns:
        User | UserErrors: The result of the operation.

    """
    request: Request | WebSocket = info.context["request"]
    container = info.context.get("container")
    service = container.get(UserService)

    try:
        token = extract_bearer_token(request)
    except AuthorizationError as e:
        return UserErrors.from_exception(e)

    try:
        user = service.get_by_token(token)
    except TokenVerificationError as e:
        return UserErrors.from_exception(e)

    return User.from_entity(user)


def create_user(
    input: UserInput,  # noqa: A002
    info: Info,  # noqa: A002
) -> UserCreationResult | UserErrors:
    """Creates a new user and returns a token.

    Args:
        input (UserInput): The input data.
        info (Info): The query info.

    Returns:
        UserCreationResult | UserErrors: The result of the operation.

    """
    validated_input = input.to_pydantic()
    container = info.context.get("container")
    service = container.get(UserService)

    try:
        token = service.create(validated_input.username, validated_input.password)
    except UserCreationError as e:
        return UserErrors.from_exception(e)

    return UserCreationResult.from_entity(token)
