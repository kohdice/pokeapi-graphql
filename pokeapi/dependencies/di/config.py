from injector import Binder, Module, singleton

from pokeapi.dependencies.settings import AppConfig, AppConfigABC


class ConfigModule(Module):
    """The configuration module.

    This class is responsible for providing the configuration to the application.

    """

    def configure(self, binder: Binder) -> None:
        """Configure the module.

        Args:
            binder (Binder): The binder to configure.

        """
        binder.bind(AppConfigABC, to=AppConfig, scope=singleton)  # type: ignore[type-abstract]
