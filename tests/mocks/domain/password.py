from injector import singleton

from pokeapi.domain.services.password_abc import PasswordServiceABC


@singleton
class MockPasswordService(PasswordServiceABC):
    @staticmethod
    def hash(password: str) -> str:
        return "password"

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        if password == "password":
            return True

        return False
