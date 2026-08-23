import time
from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditUserLocalName(BaleMethod):
    """
    Edits the local name of a user.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.USER.value
    __method__ = "EditUserLocalName"

    __returning__ = DefaultResponse

    user_id: int = Field(..., alias="1")
    """
    The unique identifier of the user whose local name is being edited.
    """

    access_hash: int = Field(..., alias="2")
    """
    The access hash of the user, used for authorization purposes.
    """

    name: str = Field(..., alias="3")
    """
    The new local name to assign to the user.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            name: str,
            access_hash: int,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                name=name, user_id=user_id, access_hash=access_hash, **__pydantic_kwargs
            )
