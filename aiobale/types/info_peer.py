from typing import TYPE_CHECKING, Optional
from pydantic import Field

from ..enums import ChatType
from .base import BaleObject


class InfoPeer(BaleObject):
    """
    Represents a minimal peer information object commonly used in Bale messaging events.

    This class typically appears in contexts where only the user ID and possibly the chat type
    are known or required (e.g., identifying who performed an action).

    Note:
        All date or time fields in the Bale API are represented as millisecond timestamps.
        Although this class currently does not have date fields, this is important for other related models.
    """

    id: int = Field(..., alias="1")
    """The unique identifier of the peer (usually user ID or chat ID)."""

    type: Optional[ChatType] = Field(None, alias="2")
    """
    The type of chat (e.g., user, group, channel).
    
    This field is optional because sometimes only the ID is provided, and type inference
    or external context is required to interpret the peer correctly.
    """

    if TYPE_CHECKING:
        # This __init__ method is only used for type checking and IDE autocomplete support.
        # It does not affect runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            type: Optional[ChatType] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                id=id,
                type=type,
                **__pydantic_kwargs
            )
