from .base import BaseEntity


class User(BaseEntity):
    """Entity class of User.

    Attributes:
        id_ (int): The unique identifier for the User.
        username (str): The username of the User.
        password (str): The password of the User.

    """

    id_: int = 0
    username: str
    password: str
