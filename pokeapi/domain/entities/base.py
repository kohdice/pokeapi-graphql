from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    """Base class for domain entities.

    This class provides a base class for domain entities. It inherits from Pydantic's
    BaseModel class, and can be used as a base class for all domain entities.

    Attributes:
        model_config (ConfigDict): The configuration for the Pydantic model.

    """

    model_config = ConfigDict(validate_assignment=True, frozen=True)
