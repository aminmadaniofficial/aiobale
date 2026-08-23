from typing import TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject
from ..upvote import Upvote


class UpvoteResponse(BaleObject):
    """
    Represents the response containing upvote-related information.
    """

    upvote: Upvote = Field(..., alias="1")
    """Details of the upvote action."""

    if TYPE_CHECKING:
        # This __init__ is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            upvote: Upvote,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(upvote=upvote, **__pydantic_kwargs)
