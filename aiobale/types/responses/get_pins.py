from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING
from pydantic import Field, model_validator

from ...enums import ChatType
from ..message_data import MessageData
from ..message import Message
from ..short_peer import ShortPeer
from ..chat import Chat
from ..base import BaleObject


class GetPinsResponse(BaleObject):
    """
    Response class representing the pinned messages in a chat.

    Attributes:
        pins_data (List[MessageData]): List of pinned message data objects. 
            This is the raw data received from the server, which includes message details.
        count (int): Total number of pinned messages available.
        method_data (Any): Additional data related to the method/request, typically includes group info.
        pins (List[Message]): Extracted pinned messages for easier access after processing.
    """

    pins_data: List[MessageData] = Field(default_factory=list, alias="1")
    """Raw pinned message data received from the server."""

    count: int = Field(0, alias="2")
    """Total count of pinned messages."""

    method_data: Any
    """Supplementary data related to the request, e.g., group information."""

    pins: List[Message] = []
    """List of extracted Message objects from pins_data after processing."""

    @model_validator(mode="before")
    @classmethod
    def normalize_lists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that 'pins_data' (alias '1') is always a list.

        Some server responses may return a single MessageData object instead of a list,
        so this method wraps it in a list for consistent downstream handling.
        """
        value = data.get("1")
        if value is not None and not isinstance(value, list):
            data["1"] = [value]
        return data

    @model_validator(mode="after")
    def add_message(self) -> GetPinsResponse:
        """
        Processes the pins_data list to:
        - Assign chat information (with group id and type) to each pinned message.
        - Populate the 'pins' field with the actual Message objects extracted from pins_data.

        Returns:
            self: The updated instance with pins populated.
        """
        group = getattr(self.method_data, "group", None)
        if not group or not isinstance(group, ShortPeer):
            return self

        for pinned in self.pins_data:
            pinned.chat = Chat(id=group.id, type=ChatType.GROUP)

        # Prevent infinite loop: bypass Pydantic
        object.__setattr__(self, "pins", [pin.message for pin in self.pins_data])
        return self

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            pins_data: List[MessageData] = ...,
            count: int = 0,
            method_data: Any = ...,
            pins: List[Message] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                pins_data=pins_data,
                count=count,
                method_data=method_data,
                pins=pins,
                **__pydantic_kwargs,
            )
