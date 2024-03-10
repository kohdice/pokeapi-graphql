from injector import singleton
from passlib.hash import argon2

from .password_abc import PasswordServiceABC


@singleton
class PasswordService(PasswordServiceABC):
    """Service to hash and verify passwords.

    This service uses the argon2 algorithm to hash and verify passwords.

    """

    @staticmethod
    def hash(password: str) -> str:
        """Hash a password using argon2.

        Args:
            password: The password to hash.

        Returns:
            The hashed password.

        """
        hashed_password = argon2.hash(password)

        # NOTE: argon2.hash returns a string, but we can't be sure of the type
        assert isinstance(hashed_password, str)

        return hashed_password

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        """Verify a password using argon2.

        Args:
            password: The password to verify.
            hashed_password: The hashed password to compare with.

        Returns:
            True if the password is verified, False otherwise.

        """
        result = argon2.verify(password, hashed_password)

        # NOTE: argon2.verify returns a boolean, but we can't be sure of the type
        assert isinstance(result, bool)

        return result
