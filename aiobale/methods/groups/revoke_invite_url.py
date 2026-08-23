from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import InviteURLResponse
from ...enums import Services
from ..base import BaleMethod


class RevokeInviteURL(BaleMethod):
    """
    Revokes an invite URL for a specific group.

    Returns:
        aiobale.types.responses.InviteURLResponse: The response containing the details of the revoked invite URL.
    """

    __service__ = Services.GROUPS.value
    __method__ = "RevokeInviteURL"

    __returning__ = InviteURLResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group for which the invite URL is being revoked.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, group: ShortPeer, **__pydantic_kwargs
        ) -> None:
            super().__init__(group=group, **__pydantic_kwargs)
