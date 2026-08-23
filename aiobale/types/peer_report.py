from typing import TYPE_CHECKING
from pydantic import Field

from ..enums import PeerSource
from .base import BaleObject
from .peer import Peer


class PeerReport(BaleObject):
    """
    
    Represents a report request for a specific peer (user or group) in the Bale platform.

    This model is typically used when the client wants to report a user or group,
    along with the context or source from which the report was initiated.
    """

    source: PeerSource = Field(..., alias="1")
    """The source from which the peer was found (e.g., dialog list, discovery tab)."""

    peer: Peer = Field(..., alias="2")
    """The target peer (user or group) that is being reported."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            source: PeerSource,
            peer: Peer,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(source=source, peer=peer, **__pydantic_kwargs)
