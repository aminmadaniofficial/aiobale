from pydantic import Field
from typing import TYPE_CHECKING, List

from ...types import ShortPeer
from ...types.responses import FullGroupResponse
from ...enums import Services
from ..base import BaleMethod


class GetFullGroup(BaleMethod):
    """
    Retrieves detailed information about a specific group.

    Returns:
        aiobale.types.responses.FullGroupResponse: The response containing full group details.
    """

    __service__ = Services.GROUPS.value
    __method__ = "GetFullGroup"

    __returning__ = FullGroupResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The identifier of the group for which detailed information is requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, **__pydantic_kwargs)
