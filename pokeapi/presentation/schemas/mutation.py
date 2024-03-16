import strawberry

from pokeapi.presentation.resolvers.authentication import auth, create_user, refresh

from . import AUTH_PAYLOAD


@strawberry.type(description="Root mutation schema.")
class Mutation:
    """Root mutation schema.

    This schema defines the root mutation operations.

    Attributes:
        auth (AUTH_PAYLOAD): Authenticates a user and returns a token.
        refresh (AUTH_PAYLOAD): Refreshes a token.
        user_create (AUTH_PAYLOAD): Creates a new user and returns a token.

    """

    auth: AUTH_PAYLOAD = strawberry.field(
        description="Authenticates a user and returns a token.",
        resolver=auth,
    )
    refresh: AUTH_PAYLOAD = strawberry.field(
        description="Refreshes a token.", resolver=refresh
    )
    user_create: AUTH_PAYLOAD = strawberry.field(
        description="Creates a new user and returns a token.", resolver=create_user
    )
