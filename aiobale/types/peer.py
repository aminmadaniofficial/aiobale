from typing import Optional, TYPE_CHECKING
from pydantic import Field

from ..enums import PeerType
from .base import BaleObject


class Peer(BaleObject):
    """
    Represents a unique identifier for an entity in Bale (user, group, or bot).

    The `Peer` class is a fundamental object used to reference other entities in the Bale platform.
    It combines an entity type with its ID and optionally an access hash for secure identification.
    """

    type: PeerType = Field(..., alias="1")
    """The type of the peer (e.g., user, group, bot)."""

    id: int = Field(..., alias="2")
    """The unique ID of the peer within its type category."""

    access_hash: Optional[int] = Field(None, alias="3")
    """
    An optional hash used for secure access to the peer. 
    This is typically required for accessing peers outside the current user’s contact list.
    """

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type: PeerType,
            id: int,
            access_hash: Optional[int] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(type=type, id=id, access_hash=access_hash, **__pydantic_kwargs)
