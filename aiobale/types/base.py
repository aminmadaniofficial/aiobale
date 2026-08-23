from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

from ..client.context_controller import BotContextController


class BaleObject(BotContextController, BaseModel):
    """
    A base class for Bale objects that combines `BotContextController` and `BaseModel`.
    This class provides configuration for Pydantic models and extends functionality
    with custom JSON encoders and validation rules.
    """

    model_config = ConfigDict(
        populate_by_name=True,  # Allows population of fields by their alias or name.
        use_enum_values=True,  # Automatically converts enums to their values.
        extra="allow",  # Allows extra fields not explicitly defined in the model.
        validate_assignment=True,  # Validates fields on assignment.
        arbitrary_types_allowed=True,  # Allows arbitrary types in the model.
        defer_build=True,  # Defers model building for performance optimization.
        json_encoders={
            bool: lambda v: 1 if v else 0  # Encodes boolean values as 1 (True) or 0 (False).
        }
    )

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *args,
            **kwargs
        ) -> None:
            super().__init__(*args, **kwargs)
