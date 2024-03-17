import logging

from injector import inject, singleton
from sqlalchemy import and_, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pokeapi.domain.entities.user import User as UserEntity
from pokeapi.domain.repositories.user import UserRepositoryABC
from pokeapi.exceptions.user import UserCreationError, UserUpdateError
from pokeapi.infrastructure.database.models import User as UserModel


@singleton
class UserRepository(UserRepositoryABC):
    """Concrete implementation of the user repository.

    This class provides an implementation of the user repository interface. It uses
    SQLAlchemy to interact with the database.

    Attributes:
        _logger (Logger): The logger instance used by the repository.
        _db (Session): The database session to be used by the repository.

    """

    @inject
    def __init__(self, db: Session) -> None:
        """Initializer for UserRepository.

        Args:
            db (Session): The database session object used by the repository.

        """
        self._logger = logging.getLogger(__name__)
        self._db = db

    def _convert_to_entity(self, model: UserModel) -> UserEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity
        instance.

        Args:
            model (UserModel): The SQLAlchemy model instance to be converted.

        Returns:
            UserEntity: The domain entity instance.

        """
        return UserEntity(
            id_=model.id_,
            username=model.username,
            password=model.password,
        )

    def get_by_id(self, id_: int) -> UserEntity | None:
        """Retrieve an entity by its identifier.

        Args:
            id_ (int): The identifier of the entity to retrieve.

        Returns:
            UserEntity | None: The entity with the specified identifier, or None if not found.

        """
        statement = select(UserModel).where(
            and_(UserModel.id_ == id_, UserModel.deleted_at.is_(None))
        )
        result = self._db.execute(statement).scalar()

        if result is None:
            return None

        return self._convert_to_entity(result)

    def get_by_username(self, username: str) -> UserEntity | None:
        """Retrieve an entity by its username.

        Args:
            username (str): The username of the entity to retrieve.

        Returns:
            UserEntity | None: The entity with the specified username, or None if not found.

        """
        statement = select(UserModel).where(
            and_(UserModel.username == username, UserModel.deleted_at.is_(None))
        )
        result = self._db.execute(statement).scalar()

        if result is None:
            return None

        return self._convert_to_entity(result)

    def create(self, entity: UserEntity) -> UserEntity:
        """Create a new entity.

        Args:
            entity (BaseEntity): The entity to be created.

        Returns:
            BaseEntity: The created entity.

        Raises:
            UserCreationError: If an error occurs while creating the entity.

        """
        statement = insert(UserModel).values(
            username=entity.username,
            password=entity.password,
            created_by=entity.username,
            updated_by=entity.username,
        )

        try:
            result = self._db.execute(statement)
            self._db.commit()
        except IntegrityError as e:
            self._db.rollback()
            self._logger.error(e)
            raise UserCreationError("Failed to create user") from None

        if result.inserted_primary_key is None:
            raise UserCreationError("Failed to create user")

        read_statement = select(UserModel).where(
            UserModel.id_ == result.inserted_primary_key[0]
        )
        created_user = self._db.execute(read_statement).scalar_one()

        return self._convert_to_entity(created_user)

    def update(self, entity: UserEntity) -> UserEntity:
        """Update an entity.

        Args:
            entity (BaseEntity): The entity to be updated.

        Raises:
            UserUpdateError: If an error occurs while updating the entity.

        """
        statement = (
            update(UserModel)
            .where(UserModel.id_ == entity.id_)
            .values(
                username=entity.username,
                password=entity.password,
                updated_by=entity.username,
            )
        )

        try:
            result = self._db.execute(statement)
            self._db.commit()
        except IntegrityError as e:
            self._db.rollback()
            self._logger.error(e)
            raise UserUpdateError("Failed to update user") from None

        if result.rowcount == 0:
            self._logger.error(
                UserUpdateError(f"Failed to update user. user_id: {entity.id_}")
            )
            raise UserUpdateError("Failed to update user.")

        read_statement = select(UserModel).where(UserModel.id_ == entity.id_)
        updated_user = self._db.execute(read_statement).scalar_one()

        return self._convert_to_entity(updated_user)
