from typing import TYPE_CHECKING
from pydantic import Field

from .base import BaleObject


class ShortPeer(BaleObject):
    """
    Represents a minimal peer identifier used primarily for group-related requests in Bale.

    This class encapsulates the unique ID of the peer (e.g., user or group)
    along with an access hash that serves as a security token to validate permissions.
    """

    id: int = Field(..., alias="1")
    """The unique identifier of the peer (e.g., group ID or user ID)."""

    access_hash: int = Field(1, alias="2")
    """A security hash used to authorize access to the peer.  
    Defaults to 1 when no specific access hash is provided."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            access_hash: int = 1,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(id=id, access_hash=access_hash, **__pydantic_kwargs)
