import logging

from starlette.requests import Request
from starlette.websockets import WebSocket

from pokeapi.exceptions.authorization import (
    AuthorizationError,
    InvalidAuthorizationHeaderError,
    NoAuthorizationHeaderError,
)

LOGGER = logging.getLogger(__name__)


def extract_bearer_token(request: Request | WebSocket) -> str:
    """Extracts the bearer token from the request's authorization header.

    Args:
        request (Request | WebSocket): The request object.

    Returns:
        str: The bearer token.

    Raises:
        AuthorizationError: If the authorization header is missing or invalid.

    """
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        LOGGER.error(
            NoAuthorizationHeaderError(
                "Authorization header does not contain a bearer token."
            )
        )
        raise AuthorizationError("User is unauthorized.")

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        LOGGER.error(
            InvalidAuthorizationHeaderError(f"Invalid authorization header: {parts}")
        )
        raise AuthorizationError("User is unauthorized.")

    return parts[1]
