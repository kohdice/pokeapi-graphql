import datetime
from abc import ABC, abstractmethod

from pokeapi.domain.entities.base import BaseEntity
from pokeapi.infrastructure.database.models.base import BaseModel


class TokenWhitelistRepositoryABC(ABC):
    """Abstract base class for sample repositories.

    This class defines the interface for token whitelist repositories. Concrete implementations
    should inherit from this class and provide
    implementations for the abstract methods.

    """

    @abstractmethod
    def _convert_to_entity(self, model: BaseModel) -> BaseEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (BaseModel): The SQLAlchemy model instance to be converted.

        Returns:
            BaseEntity: The converted instance of the domain entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_access_token(
        self, entity: BaseEntity, expiration: datetime.datetime
    ) -> BaseEntity | None:
        """Retrieve an entity by its access token.

        Args:
            access_token (str): The access token of the entity to retrieve.

        Returns:
            entity (BaseEntity): The entity with the specified access token.
            expiration (datetime.datetime): The expiration date of the access token.

        """
        pass  # pragma: no cover

    @abstractmethod
    def get_by_refresh_token(
        self, entity: BaseEntity, expiration: datetime.datetime
    ) -> BaseEntity | None:
        """Retrieve an entity by its refresh token.

        Args:
            refresh_token (str): The refresh token of the entity to retrieve.

        Returns:
            entity (BaseEntity): The entity with the specified refresh token.
            expiration (datetime.datetime): The expiration date of the refresh token.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, entity: BaseEntity) -> None:
        """Create a new entity.

        Args:
            entity (BaseEntity): The entity to be created.

        Returns:
            BaseEntity: The created entity.

        """
        pass  # pragma: no cover

    @abstractmethod
    def update(self, entity: BaseEntity) -> None:
        """Update an entity.

        Args:
            entity (BaseEntity): The entity to be updated.

        Returns:
            BaseEntity: The updated entity.

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
