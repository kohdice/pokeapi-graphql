from injector import inject, singleton
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.domain.repositories.pokemon_type import TypeRepositoryABC
from pokeapi.infrastructure.database.models.type_mst import TypeMst


@singleton
class TypeRepository(TypeRepositoryABC):
    """Repository for PokemonType

    This class implements the TypeRepositoryABC abstract base class and provides
    methods to interact with the database.

    Attributes:
        _db (Session): Database session

    """

    @inject
    def __init__(self, db: Session) -> None:
        """Initializer for TypeRepository

        Args:
            db (Session): Database session

        """
        self._db = db

    def _convert_to_entity(self, model: TypeMst) -> PokemonType:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity

        Args:
            model (TypeMst): The SQLAlchemy model instance of Type to be converted.

        Returns:
            PokemonType: The converted instance of the domain entity of Type.

        """
        return PokemonType(
            id_=model.id_,
            name=model.type_,
        )

    def get_by_id(self, id_: int) -> PokemonType | None:
        """Retrieve a type by its identifier.

        Args:
            id_ (int): The identifier of the type to retrieve.

        Returns:
            PokemonType | None: The type with the specified identifier, or None if not found.

        """
        statement = select(TypeMst).where(
            and_(TypeMst.id_ == id_, TypeMst.deleted_at.is_(None))
        )
        result = self._db.execute(statement).scalar()

        if result is None:
            return None

        return self._convert_to_entity(result)

    def get_all(self) -> list[PokemonType]:
        """Retrieve all types.

        Returns:
            list[PokemonType]: A list of all types.

        """
        statement = select(TypeMst).where(TypeMst.deleted_at.is_(None))
        results = self._db.execute(statement).scalars().all()

        return [self._convert_to_entity(result) for result in results]
