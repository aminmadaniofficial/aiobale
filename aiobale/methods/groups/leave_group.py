from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class LeaveGroup(BaleMethod):
    """
    Leaves a specified group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "LeaveGroup"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group to leave, represented as a ShortPeer object.
    """

    random_id: int = Field(..., alias="2")
    """
    A unique random identifier for the request to ensure idempotency.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, random_id: int, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, random_id=random_id, **__pydantic_kwargs)
