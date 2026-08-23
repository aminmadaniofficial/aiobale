from __future__ import annotations

from typing import List, Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..message_views import MessageViews


class ViewsResponse(BaleObject):
    """
    Response model containing the views information of multiple messages.

    Attributes:
        messages (List[MessageViews]): List of message view details.
            Ensured to be always a list, even if a single item is returned from the server.
    """

    messages: List[MessageViews] = Field(default_factory=list, alias="1")
    """List of message view objects."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the 'messages' field (alias '1') to always be a list.

        This handles cases where the server might return a single item instead of a list.
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
            messages: List[MessageViews] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(messages=messages, **__pydantic_kwargs)
