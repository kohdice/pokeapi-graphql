from abc import ABC, abstractmethod


class PasswordServiceABC(ABC):
    """Abstract class for password hashing and verification

    This class is an abstract class that defines the methods that a password hashing
    and verification service should

    """

    @staticmethod
    @abstractmethod
    def hash(password: str) -> str:
        """Hash a password

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.

        """
        pass  # pragma: no cover

    @staticmethod
    @abstractmethod
    def verify(password: str, hashed_password: str) -> bool:
        """Verify a password

        Args:
            password (str): The password to be verified.
            hashed_password (str): The hashed password to be compared with.

        Returns:
            bool: True if the password is verified, False otherwise.

        """
        pass  # pragma: no cover
