from __future__ import annotations

from pydantic import Field, model_validator
from typing import Any, Dict, List, TYPE_CHECKING

from .base import BaleObject
from .reaction import Reaction


class MessageReactions(BaleObject):
    """
    Represents the reactions associated with a specific message in Bale.

    This includes the unique message ID, the timestamp of the message, and a list
    of user reactions to that message.

    Note:
        All timestamps are represented as Unix timestamps in **milliseconds**.
    """

    id: int = Field(..., alias="1")
    """
    The unique identifier of the message this reaction data is related to.
    Used to associate reactions with their corresponding message.
    """

    date: int = Field(..., alias="2")
    """
    The timestamp when the message was sent, represented as milliseconds since the Unix epoch.
    Important for ordering and filtering reactions based on message time.
    """

    reactions: List[Reaction] = Field(default_factory=list, alias="3")
    """
    A list of Reaction objects representing individual user reactions to the message.

    Even if a single reaction exists, this field is always a list internally.
    """

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that the 'reactions' field (alias "3") is always a list,
        even if the raw input provides a single Reaction object.

        This is necessary because the API sometimes returns a single item
        instead of a list of items.
        """
        if "3" not in data:
            return data
        
        if not isinstance(data["3"], list):
            data["3"] = [data["3"]]
        
        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            date: int,
            reactions: List[Reaction] = ...,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(id=id, date=date, reactions=reactions, **__pydantic_kwargs)
