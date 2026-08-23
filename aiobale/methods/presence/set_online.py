from pydantic import Field
from typing import TYPE_CHECKING

from ...types import IntBool
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SetOnline(BaleMethod):
    """
    Sets the online presence status of the user.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.PRESENCE.value
    __method__ = "SetOnline"

    __returning__ = DefaultResponse

    is_online: IntBool = Field(..., alias="1")
    """
    Indicates whether the user is online or offline.
    Accepts an IntBool (integer representation of a boolean value).
    """

    timeout: int = Field(..., alias="2")
    """
    The duration (in seconds) for which the online status should be maintained.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, is_online: bool, timeout: int, **__pydantic_kwargs
        ) -> None:
            super().__init__(is_online=is_online, timeout=timeout, **__pydantic_kwargs)
