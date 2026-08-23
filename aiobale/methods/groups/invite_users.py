from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer
from ...types.responses import InviteResponse
from ...enums import Services
from ..base import BaleMethod


class InviteUsers(BaleMethod):
    """
    Invites users to a specified group.

    Returns:
        aiobale.types.responses.InviteResponse: The response indicating the result of the invitation process.
    """

    __service__ = Services.GROUPS.value
    __method__ = "InviteUsers"

    __returning__ = InviteResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group to which the users are being invited.
    """

    random_id: int = Field(..., alias="2")
    """
    A unique random identifier to ensure idempotency of the request.
    """

    users: List[ShortPeer] = Field(..., alias="3")
    """
    The list of users to be invited to the group.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            random_id: int,
            users: List[ShortPeer],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id, group=group, users=users, **__pydantic_kwargs
            )
