from injector import inject, singleton
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from pokeapi.domain.entities.pokemon_ability import PokemonAbility
from pokeapi.domain.repositories.pokemon_ability import AbilityRepositoryABC
from pokeapi.infrastructure.database.models.ability_mst import AbilityMst


@singleton
class AbilityRepository(AbilityRepositoryABC):
    """Repository for PokemonAbility

    This class implements the AbilityRepositoryABC abstract base class and provides
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

    def _convert_to_entity(self, model: AbilityMst) -> PokemonAbility:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity

        Args:
            model (AbilityMst): The SQLAlchemy model instance of Ability to be converted.

        Returns:
            PokemonType: The converted instance of the domain entity of Ability.

        """
        return PokemonAbility(
            id_=model.id_,
            name=model.ability,
        )

    def get_by_id(self, id_: int) -> PokemonAbility | None:
        """Retrieve a ability by its identifier.

        Args:
            id_ (int): The identifier of the ability to retrieve.

        Returns:
            PokemonAbility | None: The ability with the specified identifier, or None if not found.

        """
        statement = select(AbilityMst).where(
            and_(AbilityMst.id_ == id_, AbilityMst.deleted_at.is_(None))
        )
        result = self._db.execute(statement).scalar()

        if result is None:
            return None

        return self._convert_to_entity(result)

    def get_all(self) -> list[PokemonAbility]:
        """Retrieve all abilities.

        Returns:
            list[PokemonAbility]: A list of all abilities.

        """
        statement = select(AbilityMst).where(AbilityMst.deleted_at.is_(None))
        results = self._db.execute(statement).scalars().all()

        return [self._convert_to_entity(result) for result in results]
