import datetime
import logging

from sqlalchemy import and_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pokeapi.domain.entities.token_whitelist import (
    TokenWhitelist as TokenWhitelistEntity,
)
from pokeapi.domain.repositories.token_whitelist import TokenWhitelistRepositoryABC
from pokeapi.exceptions.token import TokenRegistrationError, TokenUpdateError
from pokeapi.infrastructure.database.models.token_whitelist import (
    TokenWhitelist as TokenWhitelistModel,
)


class TokenWhitelistRepository(TokenWhitelistRepositoryABC):
    """Concrete implementation of the token whitelist repository.

        This class provides an implementation of the token whitelist repository interface using
        SQLAlchemy as the data store.

    Attributes:
        _db (Session): The SQLAlchemy session object.

    """

    def __init__(self, db: Session) -> None:
        """Initializes the token whitelist repository.

        Args:
            db (Session): The SQLAlchemy session object.

        """
        self._db = db
        self._logger = logging.getLogger(__name__)

    def _convert_to_entity(self, model: TokenWhitelistModel) -> TokenWhitelistEntity:  # type: ignore
        """Converts a SQLAlchemy model to a domain entity.

        Args:
            model (TokenWhitelistModel): The SQLAlchemy model instance to be converted.

        Returns:
            TokenWhitelistEntity: The converted instance of the domain entity.

        """
        return TokenWhitelistEntity(
            id_=model.id_,
            user_id=model.user_id,
            access_token=model.access_token,
            refresh_token=model.refresh_token,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_by=model.updated_by,
            updated_at=model.updated_at,
        )

    def get_by_access_token(  # type: ignore
        self, entity: TokenWhitelistEntity, expiration: datetime.datetime
    ) -> TokenWhitelistEntity | None:
        """Retrieve an entity by its access token.

        Args:
            entity (TokenWhitelistEntity): The entity with the access token to retrieve.
            expiration (datetime.datetime): The expiration date of the access token.

        Returns:
            TokenWhitelistEntity: The entity with the specified access token.

        """
        statement = select(TokenWhitelistModel).where(
            and_(
                TokenWhitelistModel.user_id == entity.user_id,
                TokenWhitelistModel.access_token == entity.access_token,
                TokenWhitelistModel.updated_at.between(
                    expiration, datetime.datetime.now()
                ),
                TokenWhitelistModel.deleted_at.is_(None),
            )
        )
        result = self._db.execute(statement).scalar()

        if result is None:
            return None

        return self._convert_to_entity(result)

    def get_by_refresh_token(  # type: ignore
        self, entity: TokenWhitelistEntity, expiration: datetime.datetime
    ) -> TokenWhitelistEntity | None:
        """Retrieve an entity by its refresh token.

        Args:
            entity (TokenWhitelistEntity): The entity with the refresh token to retrieve.
            expiration (datetime.datetime): The expiration date of the refresh token.

        Returns:
            TokenWhitelistEntity: The entity with the specified refresh token.

        """
        statement = select(TokenWhitelistModel).where(
            and_(
                TokenWhitelistModel.user_id == entity.user_id,
                TokenWhitelistModel.refresh_token == entity.refresh_token,
                TokenWhitelistModel.updated_at.between(
                    expiration, datetime.datetime.now()
                ),
                TokenWhitelistModel.deleted_at.is_(None),
            )
        )
        result = self._db.execute(statement).scalar()

        if result is None:
            return None

        return self._convert_to_entity(result)

    def create(self, entity: TokenWhitelistEntity) -> None:  # type: ignore
        """Create a new entity.

        Args:
            entity (TokenWhitelistEntity): The entity to be created.

        Raises:
            TokenRegistrationError: If the entity could not be created.

        """
        statement = TokenWhitelistModel(
            user_id=entity.user_id,
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_by=entity.updated_by,
            updated_at=entity.updated_at,
        )
        try:
            self._db.add(statement)
            self._db.commit()
        except IntegrityError as e:
            self._db.rollback()
            self._logger.error(f"Failed to register token in the whitelist : {e}")
            raise TokenRegistrationError("Failed to register token") from None

    def update(self, entity: TokenWhitelistEntity) -> None:  # type: ignore
        """Update an existing entity.

        Args:
            entity (TokenWhitelistEntity): The entity to be updated.

        Raises:
            TokenUpdateError: If the entity could not be updated.

        """
        statement = (
            update(TokenWhitelistModel)
            .where(TokenWhitelistModel.user_id == entity.user_id)
            .values(
                access_token=entity.access_token,
                refresh_token=entity.refresh_token,
                updated_by=entity.updated_by,
                updated_at=entity.updated_at,
            )
        )
        result = self._db.execute(statement)

        if result.rowcount == 0:
            self._db.rollback()
            self._logger.error(
                f"Faild to update token. ID: {entity.id_}, User: {entity.user_id}"
            )
            raise TokenUpdateError("Failed to update token") from None

        self._db.commit()

    def delete(self, user_id: int, expiration: datetime.datetime) -> None:  # type: ignore
        """Delete expired tokens for a user.

        Args:
            user_id (int): The user ID for which to delete expired tokens.
            expiration (datetime.datetime): The expiration date for the tokens to be deleted.

        """
        statement = (
            update(TokenWhitelistModel)
            .where(
                and_(
                    TokenWhitelistModel.user_id == user_id,
                    TokenWhitelistModel.updated_at <= expiration,
                    TokenWhitelistModel.deleted_at.is_(None),
                )
            )
            .values(deleted_at=datetime.datetime.now())
        )

        result = self._db.execute(statement)
        self._db.commit()
        self._logger.info(
            f"Deleted {result.rowcount} expired tokens for user: {user_id}"
        )