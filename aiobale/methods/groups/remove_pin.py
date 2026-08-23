from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class RemoveAllPins(BaleMethod):
    """
    Removes all pinned messages from a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "RemovePin"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which all pinned messages will be removed.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, **__pydantic_kwargs)
