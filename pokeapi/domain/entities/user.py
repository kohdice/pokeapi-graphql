from pokeapi.domain.entities.base import BaseEntity


class User(BaseEntity):
    """Entity class of User.

    Attributes:
        id_ (int): The unique identifier for the User.
        username (str): The username of the User.
        password (str): The password of the User.

    """

    id_: int | None
    username: str
    password: str
