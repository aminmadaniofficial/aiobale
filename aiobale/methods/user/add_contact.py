from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class AddContact(BaleMethod):
    """
    Adds a new contact to the user's contact list.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.USER.value
    __method__ = "AddContact"

    __returning__ = DefaultResponse

    user_id: int = Field(..., alias="1")
    """
    The unique identifier of the user to be added as a contact.
    """

    type: int = Field(1, alias="2")
    """
    The type of contact being added. Defaults to 1.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, user_id: int, type: int = 1, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(user_id=user_id, type=type, **__pydantic_kwargs)
