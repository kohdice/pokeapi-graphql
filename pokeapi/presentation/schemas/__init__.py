from typing import Annotated

import strawberry

from .authentication import AuthErrors, AuthResult
from .user import User, UserCreationResult, UserErrors

AUTH_PAYLOAD = Annotated[
    AuthResult | AuthErrors,
    strawberry.union("AuthPayload", description="Union of AuthResult and AuthErrors."),
]
USER_PAYLOAD = Annotated[
    User | UserErrors,
    strawberry.union("UserPayload", description="Union of User and UserErrors."),
]
USER_CREATION_PAYLOAD = Annotated[
    UserCreationResult | UserErrors,
    strawberry.union(
        "UserCreationPayload", description="Union of UserCreationResult and UserErrors."
    ),
]
