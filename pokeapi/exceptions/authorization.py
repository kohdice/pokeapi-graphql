class AuthorizationError(Exception):
    """Raised when the user is unauthorized."""


class InvalidAuthorizationHeaderError(Exception):
    """Raised when the request contains an invalid authorization header."""


class NoAuthorizationHeaderError(Exception):
    """Raised when the request does not contain an authorization header."""
