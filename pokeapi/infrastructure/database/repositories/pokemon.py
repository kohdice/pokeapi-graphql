from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from pokeapi.domain.entities.pokemon import Pokemon as PokemonEntity
from pokeapi.domain.entities.pokemon_ability import PokemonAbility
from pokeapi.domain.entities.pokemon_stats import PokemonStats
from pokeapi.domain.entities.pokemon_type import PokemonType
from pokeapi.domain.entities.pokemons_ability import PokemonsAbility
from pokeapi.domain.entities.pokemons_type import PokemonsType
from pokeapi.domain.repositories.pokemon import PokemonRepositoryABC
from pokeapi.infrastructure.database.models.pokemon_mst import Pokemon as PokemonModel


class PokemonRepository(PokemonRepositoryABC[PokemonModel, PokemonEntity]):
    def __init__(self, db: Session) -> None:
        """Initializer for PokemonRepository.

        Args:
            db (Session): The database session object used by the repository.

        """

        super().__init__(db)

    def _convert_to_entity(self, model: PokemonModel) -> PokemonEntity:
        """Converts a SQLAlchemy model to a domain entity.

        This method converts a SQLAlchemy model instance to a corresponding domain entity

        Args:
            model (PokemonModel): The SQLAlchemy model instance of Pokémon to be converted.

        Returns:
            PokemonEntity: The converted instance of the domain entity of Pokémon.

        """
        stats = PokemonStats(
            hp=model.hp,
            attack=model.attack,
            defense=model.defense,
            special_attack=model.special_attack,
            special_defense=model.special_defense,
            speed=model.speed,
            base_total=model.base_total,
        )

        pokemons_type = (
            PokemonsType(
                pokemon_type=PokemonType(id_=type_.type_.id_, name=type_.type_.type_),
                slot=type_.slot,
            )
            for type_ in model.pokemon_types
        )

        pokemons_ability = (
            PokemonsAbility(
                pokemon_ability=PokemonAbility(
                    id_=ability.ability.id_, name=ability.ability.ability
                ),
                slot=ability.slot,
                is_hidden=ability.is_hidden,
            )
            for ability in model.pokemon_abilities
        )

        return PokemonEntity(
            id_=model.id_,
            national_pokedex_number=model.national_pokedex_number,
            name=model.name,
            stats=stats,
            pokemons_type=pokemons_type,
            pokemons_ability=pokemons_ability,
        )

    def get_by_id(self, id_: int) -> PokemonEntity | None:
        """Retrieve a Pokémon by its identifier.

        Args:
            id_ (int): The identifier of the Pokémon to be retrieved.

        Returns:
            PokemonEntity | None:
                The Pokémon with the specified identifier, or None if no such Pokémon exists.

        """
        statement = select(PokemonModel).where(
            and_(PokemonModel.id_ == id_, PokemonModel.deleted_at.is_(None))
        )

        result = self._db.execute(statement).scalar()

        if result is None:
            return None
        print(f"created at: {result.created_at}")

        return self._convert_to_entity(result)

    def get_all(self) -> list | list[PokemonEntity]:
        statement = select(PokemonModel).where(PokemonModel.deleted_at.is_(None))

        result = self._db.execute(statement).scalars().all()

        if not result:
            return []

        return [self._convert_to_entity(pokemon) for pokemon in result]
