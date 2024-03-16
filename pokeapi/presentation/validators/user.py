import re

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


class UserInputValidator(BaseModel):
    """Validator for the user input

    Attributes:
        username (str): The username
        password (str): The password

    """

    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=50)

    @field_validator("username", "password")
    @classmethod
    def validate_half_width_alphanumeric(cls, v: str) -> str:
        """Validate if the value is half-width alphanumeric

        Args:
            v (str): The value to validate

        Returns:
            str: The validated value

        Raises:
            PydanticCustomError: If the value is not half-width alphanumeric

        """
        pattern = r"^[a-zA-Z0-9]+$"

        if not bool(re.match(pattern, v)):
            raise PydanticCustomError(
                "not_half-width_alphanumeric",
                "Only half-width alphanumeric characters are allowed,  got '{wrong_value}'",
                dict(wrong_value=v),
            )

        return v
