class UserCreationError(Exception):
    """Raised when an error occurs while creating a user."""


class UserNotFoundError(Exception):
    """Raised when a user is not found."""


class UserUpdateError(Exception):
    """Raised when an error occurs while updating a user."""
