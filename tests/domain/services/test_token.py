import datetime
import uuid

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from freezegun import freeze_time
from injector import Injector
from jose import jwt

from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.domain.entities.user import User
from pokeapi.domain.services.token import TokenService
from pokeapi.exceptions.token import TokenVerificationError
from tests.conftest import EXECUTION_DATETIME, ISSUE_DATETIME


@pytest.fixture(scope="module")
def service(dependency_container: Injector) -> TokenService:
    config = dependency_container.get(AppConfig)

    return TokenService(config)


@pytest.fixture(scope="module")
def dummy_private_key() -> str:
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return pem_private_key.decode("utf-8")


@pytest.fixture(scope="module")
@freeze_time(ISSUE_DATETIME)
def exp(dependency_container: Injector) -> datetime.datetime:
    config = dependency_container.get(AppConfig)
    exp = datetime.datetime.utcnow() + datetime.timedelta(
        hours=config.access_token_lifetime
    )
    return exp


@pytest.fixture(scope="module")
@freeze_time(ISSUE_DATETIME)
def iat() -> datetime.datetime:
    return datetime.datetime.utcnow()


@pytest.fixture(scope="module")
def jti() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
@freeze_time(ISSUE_DATETIME)
def access_token(
    dependency_container: Injector,
    exp: datetime.datetime,
    iat: datetime.datetime,
    jti: str,
) -> str:
    config = dependency_container.get(AppConfig)

    data = {
        "iss": config.app_domain,
        "sub": "1",
        "exp": exp.timestamp(),
        "iat": iat.timestamp(),
        "jti": jti,
        "username": "Red",
    }

    actual = jwt.encode(data, config.private_key, algorithm=config.jwt_algorithm)
    assert isinstance(actual, str)

    return actual


@pytest.fixture(scope="module")
@freeze_time(ISSUE_DATETIME)
def access_token_invalid_issuer(
    dependency_container: Injector,
    exp: datetime.datetime,
    iat: datetime.datetime,
    jti: str,
) -> str:
    config = dependency_container.get(AppConfig)

    data = {
        "iss": "hoge",
        "sub": "1",
        "exp": exp.timestamp(),
        "iat": iat.timestamp(),
        "jti": jti,
        "username": "Red",
    }

    actual = jwt.encode(data, config.private_key, algorithm=config.jwt_algorithm)
    assert isinstance(actual, str)

    return actual


@pytest.fixture(scope="module")
@freeze_time(ISSUE_DATETIME)
def access_token_invalid_signature(
    dependency_container: Injector,
    dummy_private_key: str,
    exp: datetime.datetime,
    iat: datetime.datetime,
    jti: str,
) -> str:
    config = dependency_container.get(AppConfig)

    data = {
        "iss": config.app_domain,
        "sub": "1",
        "exp": exp.timestamp(),
        "iat": iat.timestamp(),
        "jti": jti,
        "username": "Red",
    }

    actual = jwt.encode(data, dummy_private_key, algorithm=config.jwt_algorithm)
    assert isinstance(actual, str)

    return actual


@pytest.fixture(scope="module")
@freeze_time(ISSUE_DATETIME)
def access_token_no_jti(
    dependency_container: Injector,
    exp: datetime.datetime,
    iat: datetime.datetime,
) -> str:
    config = dependency_container.get(AppConfig)

    data = {
        "iss": config.app_domain,
        "sub": "1",
        "exp": exp.timestamp(),
        "iat": iat.timestamp(),
        "username": "Red",
    }

    actual = jwt.encode(data, config.private_key, algorithm=config.jwt_algorithm)
    assert isinstance(actual, str)

    return actual


class TestTokenServices:
    @freeze_time(ISSUE_DATETIME)
    def test_create_token(
        self,
        service: TokenService,
        exp: datetime.datetime,
        jti: str,
        access_token: str,
    ) -> None:
        user = User(id_=1, username="Red", password="password")
        token = service.create_token(user, exp, jti)

        assert token == access_token

    @freeze_time(EXECUTION_DATETIME)
    def test_decode_token(
        self,
        dependency_container: Injector,
        service: TokenService,
        exp: datetime.datetime,
        iat: datetime.datetime,
        jti: str,
        access_token: str,
    ) -> None:
        config = dependency_container.get(AppConfig)
        actual = service.decode_token(access_token)

        assert actual["iss"] == config.app_domain
        assert actual["sub"] == "1"
        assert actual["exp"] == exp.timestamp()
        assert actual["iat"] == iat.timestamp()
        assert actual["jti"] == jti
        assert actual["username"] == "Red"

    @freeze_time(EXECUTION_DATETIME)
    def test_decode_invalid_issuer(
        self, service: TokenService, access_token_invalid_issuer: str
    ) -> None:
        with pytest.raises(TokenVerificationError):
            service.decode_token(access_token_invalid_issuer)

    def test_decode_invalid_expired(
        self, service: TokenService, access_token: str
    ) -> None:
        with pytest.raises(TokenVerificationError):
            service.decode_token(access_token)

    @freeze_time(EXECUTION_DATETIME)
    def test_decode_invalid_signature(
        self, service: TokenService, access_token_invalid_signature: str
    ) -> None:
        with pytest.raises(TokenVerificationError):
            service.decode_token(access_token_invalid_signature)

    @freeze_time(EXECUTION_DATETIME)
    def test_decode_no_jti(
        self, service: TokenService, access_token_no_jti: str
    ) -> None:
        with pytest.raises(TokenVerificationError):
            service.decode_token(access_token_no_jti)
