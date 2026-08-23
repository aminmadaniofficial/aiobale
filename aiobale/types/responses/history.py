from __future__ import annotations

from typing import List, Dict, Any, TYPE_CHECKING
from pydantic import Field, model_validator

from ..message_data import MessageData
from ..base import BaleObject
from ..chat import Chat


class HistoryResponse(BaleObject):
    """
    Represents the response containing a list of message history data.

    This class holds the list of messages retrieved from a history API call.
    It normalizes the incoming data to ensure the 'data' field is always a list,
    and provides a helper method to associate all messages with a given chat.
    """

    data: List[MessageData] = Field(default_factory=list, alias="1")
    """
    List of messages in the history.

    This field is always a list. If the server returns a single message,
    it will be wrapped in a list automatically.
    """

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validator that ensures the 'data' field (alias "1") is always a list.

        Sometimes the API might return a single message object instead of a list.
        This method wraps single objects into a list for consistent downstream processing.
        """
        if "1" not in data:
            return data

        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        return data

    def add_chat(self, chat: Chat) -> None:
        """
        Associates all messages in the history with the given Chat object.

        This sets the `chat` attribute of each message and any replied-to message,
        enabling easy access to chat-related metadata directly from messages.
        """
        for message in self.data:
            message.chat = chat
            if message.replied_to is not None:
                message.replied_to.chat = chat

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            data: List[MessageData] = ...,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(data=data, **__pydantic_kwargs)
