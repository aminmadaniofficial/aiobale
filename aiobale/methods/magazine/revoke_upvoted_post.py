from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import InfoMessage, IntValue
from ...types.responses import UpvoteResponse
from ...enums import Services
from ..base import BaleMethod


class RevokeUpvotedPost(BaleMethod):
    """
    Represents a request to revoke an upvote from a specific post or album.
    """

    __service__ = Services.MAGAZINE.value
    __method__ = "RevokeUpvotedPost"

    __returning__ = UpvoteResponse

    message: InfoMessage = Field(..., alias="1")
    """The message (post) from which the upvote should be removed."""

    album_id: Optional[IntValue] = Field(None, alias="2")
    """The album ID if the upvote relates to a specific album, otherwise `None`."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: InfoMessage,
            album_id: Optional[IntValue] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(message=message, album_id=album_id, **__pydantic_kwargs)
