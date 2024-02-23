import os

import pytest
from pytest_mock import MockerFixture

from pokeapi.dependencies.settings.config import AppConfig
from pokeapi.exceptions.config import (
    InvalidEnvironmentValueError,
    UnsetEnvironmentVariableError,
)

TEST_DATABASE_URL = "mysql://root:root@db:3306/main_db?charset=utf8"


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
        mocker.patch("os.getenv", return_value=TEST_DATABASE_URL)

        assert config.database_url == TEST_DATABASE_URL

    def test_database_url_with_error(
        self, config: AppConfig, mocker: MockerFixture
    ) -> None:
        mocker.patch("os.getenv", return_value=None)

        with pytest.raises(UnsetEnvironmentVariableError):
            _ = config.database_url
