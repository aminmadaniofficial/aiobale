import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types import StringValue
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditAbout(BaleMethod):
    """
    Updates the "about" section of a user's profile.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.USER.value
    __method__ = "EditAbout"

    __returning__ = DefaultResponse

    about: StringValue = Field(..., alias="1")
    """
    The new "about" text to be set for the user's profile.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, about: StringValue, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(about=about, **__pydantic_kwargs)
