import datetime

from injector import inject, singleton

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.domain.services.token_abc import TokenServiceABC


@singleton
class MockTokenService(TokenServiceABC):
    @inject
    def __init__(self) -> None:
        pass

    def create_token(self, entity: BaseEntity, exp: datetime.datetime, jti: str) -> str:
        return "token"

    def decode_token(self, token: str) -> dict:
        return {"foo": "bar"}
