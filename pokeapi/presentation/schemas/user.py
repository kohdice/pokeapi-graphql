import strawberry

from pokeapi.presentation.validators.user import UserInputValidator


@strawberry.experimental.pydantic.input(model=UserInputValidator)
class UserInput:
    """Input for the user

    Attributes:
        username (str): The username
        password (str): The password

    """

    username: str
    password: str
