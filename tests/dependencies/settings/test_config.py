import os
from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture

from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.exceptions.config import (
    InvalidEnvironmentValueError,
    UnsetEnvironmentVariableError,
)


class TestAppConfig:
    @pytest.fixture()
    def config(self) -> AppConfig:
        return AppConfig()

    @pytest.mark.parametrize(
        ("stage", "expected"),
        [
            ("development", "development"),
            ("DEVELOPMENT", "development"),
            ("staging", "staging"),
            ("STAGING", "staging"),
            ("production", "production"),
            ("PRODUCTION", "production"),
        ],
    )
    def test_stage(
        self, config: AppConfig, mocker: MockerFixture, stage: str, expected: str
    ) -> None:
        mocker.patch("os.getenv", return_value=stage)

        assert config.stage == expected

    def test_stage_with_invalid_value(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value="hoge")
        with pytest.raises(InvalidEnvironmentValueError):
            _ = config.stage

    def test_stage_with_none(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch.object(os, "getenv", return_value=None)
        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.stage

    @pytest.mark.parametrize(
        ("debug", "expected"),
        [
            ("true", True),
            ("True", True),
            ("false", False),
            ("False", False),
            (None, False),
        ],
    )
    def test_debug(
        self, config: AppConfig, mocker: MockerFixture, debug: str, expected: bool
    ) -> None:
        mocker.patch("os.getenv", return_value=debug)

        assert config.debug is expected

    def test_database_url(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("os.getenv", return_value="test_database_url")

        assert config.database_url == "test_database_url"

    def test_database_url_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.database_url

    def test_load_private_key_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            config._load_private_key()

    def test_load_private_key(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("builtins.open", mock_open(read_data=b"private_key"))

        actual_1 = config._load_private_key()
        actual_2 = config._load_private_key()

        assert isinstance(actual_1, bytes)
        assert isinstance(actual_2, bytes)
        assert actual_1 == actual_2

    def test_private_key(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("builtins.open", mock_open(read_data=b"private_key"))

        assert isinstance(config.private_key, bytes)

    def test_load_public_key_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            config._load_public_key()

    def test_load_public_key(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("builtins.open", mock_open(read_data=b"public_key"))

        actual_1 = config._load_public_key()
        actual_2 = config._load_public_key()

        assert isinstance(actual_1, bytes)
        assert isinstance(actual_2, bytes)
        assert actual_1 == actual_2

    def test_public_key(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("builtins.open", mock_open(read_data=b"private_key"))

        assert isinstance(config.public_key, bytes)

    def test_jwt_algorithm(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("os.getenv", return_value="test_algorithm")

        assert config.jwt_algorithm == "test_algorithm"

    def test_jwt_algorithm_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.jwt_algorithm

    def test_access_token_lifetime(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value="1")

        assert config.access_token_lifetime == 1

    def test_access_token_lifetime_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.access_token_lifetime

    def test_refresh_token_lifetime(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value="1000")

        assert config.refresh_token_lifetime == 1000

    def test_refresh_token_lifetime_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.refresh_token_lifetime

    def test_app_domain(self, config: AppConfig, mocker: MockerFixture) -> None:
        mocker.patch("os.getenv", return_value="test_domain")

        assert config.app_domain == "test_domain"

    def test_app_domain_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.app_domain
