from pokeapi.domain.entities.base import BaseEntity


class TokenWhitelist(BaseEntity):
    """Entity class of TokenWhitelist.

    Attributes:
        id_ (int): The unique identifier for the TokenWhitelist.
        user_id (int): The user_id of the TokenWhitelist.
        access_token (str): The access_token of the TokenWhitelist.
        refresh_token (str): The refresh_token of the TokenWhitelist.
    """

    id_: int | None
    user_id: int
    access_token: str
    refresh_token: str
