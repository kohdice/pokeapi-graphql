class InvalidEnvironmentValueError(Exception):
    """Raised when an environment variable has an invalid value."""


class UnsetEnvironmentVariableError(Exception):
    """Raised when an environment variable is unset."""
