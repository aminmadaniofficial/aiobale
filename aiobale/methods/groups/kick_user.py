from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class KickUser(BaleMethod):
    """
    Removes a user from a group.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "KickUser"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group from which the user will be removed.
    """

    random_id: int = Field(..., alias="2")
    """
    A unique random identifier for this request to ensure idempotency.
    """

    user: ShortPeer = Field(..., alias="3")
    """
    The user to be removed from the group.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            user: ShortPeer,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group, random_id=random_id, user=user, **__pydantic_kwargs
            )
