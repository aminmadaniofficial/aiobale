from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import DefaultResponse
from ...types import StringValue
from ...enums import Services
from ..base import BaleMethod

class EditParameter(BaleMethod):
    """
    Edits a configuration parameter by specifying its key and new value.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the result of the edit operation.
    """

    __service__ = Services.CONFIGS.value
    __method__ = "EditParameter"

    __returning__ = DefaultResponse

    key: str = Field(..., alias="1")
    """
    The key of the configuration parameter to be edited.
    """

    value: StringValue = Field(..., alias="2")
    """
    The new value to assign to the specified configuration parameter.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, key: str, value: StringValue, **__pydantic_kwargs
        ) -> None:
            super().__init__(key=key, value=value, **__pydantic_kwargs)
