from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class RemoveContact(BaleMethod):
    """
    Removes a user from the contact list.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the result of the contact removal operation.
    """

    __service__ = Services.USER.value
    __method__ = "RemoveContact"

    __returning__ = DefaultResponse

    user_id: int = Field(..., alias="1")
    """
    The unique identifier of the user to be removed from the contact list.
    """

    type: int = Field(1, alias="2")
    """
    The type of removal action. Defaults to 1.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, user_id: int, type: int = 1, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(user_id=user_id, type=type, **__pydantic_kwargs)
