from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class RemoveSinglePin(BaleMethod):
    """
    Removes a single pinned message from a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "RemoveSinglePin"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which the pinned message is to be removed.
    """

    message_id: int = Field(..., alias="2")
    """
    The unique identifier of the message to be unpinned.
    """

    date: int = Field(..., alias="3")
    """
    The timestamp indicating when the unpinning action is performed.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            message_id: int,
            date: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group, date=date, message_id=message_id, **__pydantic_kwargs
            )
