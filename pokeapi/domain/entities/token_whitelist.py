import datetime

from pokeapi.domain.entities.base import BaseEntity


class TokenWhitelist(BaseEntity):
    """Entity class of TokenWhitelist.

    Attributes:
        id_ (int): The unique identifier for the TokenWhitelist.
        user_id (int): The user_id of the TokenWhitelist.
        access_token (str): The access_token of the TokenWhitelist.
        refresh_token (str): The refresh_token of the TokenWhitelist.
        created_by (str): The user who created the TokenWhitelist.
        created_at (datetime.datetime): The date and time the TokenWhitelist was created.
        updated_by (str): The user who last updated the TokenWhitelist.
        updated_at (datetime.datetime): The date and time the TokenWhitelist was last updated.
    """

    id_: int | None
    user_id: int
    access_token: str
    refresh_token: str
    created_by: str | None
    created_at: datetime.datetime | None
    updated_by: str | None
    updated_at: datetime.datetime | None
