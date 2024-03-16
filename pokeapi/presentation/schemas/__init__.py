from typing import Annotated

import strawberry

from pokeapi.presentation.schemas.authentication import AuthErrors, AuthResult

AUTH_PAYLOAD = Annotated[
    AuthResult | AuthErrors,
    strawberry.union("AuthPayload", description="Union of AuthResult and AuthErrors."),
]
