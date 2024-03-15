import datetime
from abc import ABC, abstractmethod

from pokeapi.domain.entities.token_whitelist import (
    TokenWhitelist as TokenWhitelistEntity,
)
from pokeapi.infrastructure.database.models import TokenWhitelist as TokenWhitelistModel


class TokenWhitelistRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for token whitelist repositories. Concrete implementations
    should inherit from this class and provide
    implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: TokenWhitelistModel) -> TokenWhitelistEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (TokenWhitelistModel): The SQLAlchemy model instance to be converted.

        Returns:
            TokenWhitelistEntity: The converted instance of the domain entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_access_token(
        self, token: str, expiration: datetime.datetime
    ) -> TokenWhitelistEntity | None:
        """Retrieve an entity by its access token.

        Args:
            access_token (str): The access token of the entity to retrieve.

        Returns:
            entity (TokenWhitelistEntity): The entity with the specified access token.
            expiration (datetime.datetime): The expiration date of the access token.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_refresh_token(
        self, token: str, expiration: datetime.datetime
    ) -> TokenWhitelistEntity | None:
        """Retrieve an entity by its refresh token.

        Args:
            refresh_token (str): The refresh token of the entity to retrieve.

        Returns:
            entity (TokenWhitelistEntity): The entity with the specified refresh token.
            expiration (datetime.datetime): The expiration date of the refresh token.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, entity: TokenWhitelistEntity) -> TokenWhitelistEntity:
        """Create a new entity.

        Args:
            entity (TokenWhitelistEntity): The entity to be created.

        Returns:
            TokenWhitelistEntity: The created entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, entity: TokenWhitelistEntity) -> TokenWhitelistEntity:
        """Update an entity.

        Args:
            entity (TokenWhitelistEntity): The entity to be updated.

        Returns:
            TokenWhitelistEntity: The updated entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, user_id: int, expiration: datetime.datetime) -> None:
        """Delete expired entities.

        Args:
            user_id (int): The identifier of the entity to be deleted.
            expiration (datetime.datetime): The expiration date of the entity.

        """
        pass  # pragma: no cover
