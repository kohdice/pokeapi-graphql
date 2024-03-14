import strawberry

from pokeapi.presentation.validators.user import UserInputValidator


@strawberry.experimental.pydantic.input(
    model=UserInputValidator, description="Input for the user."
)
class UserInput:
    """Input for the user

    Attributes:
        username (str): The username
        password (str): The password

    """

    username: str = strawberry.field(description="The username")
    password: str = strawberry.field(description="The password")
