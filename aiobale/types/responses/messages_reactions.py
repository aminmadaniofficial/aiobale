from __future__ import annotations

from typing import List, Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..message_reaction import MessageReactions


class ReactionsResponse(BaleObject):
    """
    Response model representing message reactions.

    Attributes:
        messages (List[MessageReactions]): A list of message reaction objects.
            Always normalized to a list to ensure consistent handling,
            even if only a single reaction is returned.
    """

    messages: List[MessageReactions] = Field(default_factory=list, alias="1")
    """List of message reactions returned by the API."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and normalizes the 'messages' field (alias '1').

        Ensures that if the server returns a single MessageReactions object
        instead of a list, it is wrapped into a list for uniform processing.
        """
        if "1" not in data:
            return data

        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            messages: List[MessageReactions] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(messages=messages, **__pydantic_kwargs)
