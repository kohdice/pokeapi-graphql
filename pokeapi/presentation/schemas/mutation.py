import strawberry

from pokeapi.presentation.resolvers.authentication import auth, refresh
from pokeapi.presentation.resolvers.user import create_user

from . import AUTH_PAYLOAD, USER_CREATION_PAYLOAD


@strawberry.type(description="Root mutation schema.")
class Mutation:
    """Root mutation schema.

    This schema defines the root mutation operations.

    Attributes:
        auth (AUTH_PAYLOAD): Authenticates a user and returns a token.
        refresh (AUTH_PAYLOAD): Refreshes a token.
        user_create (USER_CREATION_PAYLOAD): Creates a new user and returns a token.

    """

    auth: AUTH_PAYLOAD = strawberry.field(
        resolver=auth,
        description="Authenticates a user and returns a token.",
    )
    refresh: AUTH_PAYLOAD = strawberry.field(
        resolver=refresh, description="Refreshes a token."
    )
    user_create: USER_CREATION_PAYLOAD = strawberry.field(
        resolver=create_user, description="Creates a new user and returns a token."
    )
