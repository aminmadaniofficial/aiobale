from __future__ import annotations

from typing import TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject


class InviteURLResponse(BaleObject):
    """
    Response object representing an invite URL.

    This class encapsulates the invite link URL returned by the server,
    typically used to invite others to join a group, channel, or chat.
    """

    url: str = Field(..., alias="1")
    """The invite URL string."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            url: str,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(url=url, **__pydantic_kwargs)
