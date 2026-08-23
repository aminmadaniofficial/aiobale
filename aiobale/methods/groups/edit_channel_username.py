from pydantic import Field
from typing import TYPE_CHECKING

from ...types import ShortPeer
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class EditChannelUsername(BaleMethod):
    """
    Edits the username (nick) of a group channel.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the result of the edit operation.
    """

    __service__ = Services.GROUPS.value
    __method__ = "EditChannelNick"

    __returning__ = DefaultResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group/channel whose username is to be edited. Should be a valid ShortPeer instance representing the target group.
    """

    username: str = Field(..., alias="2")
    """
    The new username (nick) to assign to the group/channel. Must be a valid string conforming to username requirements.
    """

    random_id: int = Field(..., alias="3")
    """
    A random identifier used for request uniqueness and idempotency. Should be a unique integer for each request.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            username: str,
            random_id: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id, group=group, username=username, **__pydantic_kwargs
            )
