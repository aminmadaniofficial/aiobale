from __future__ import annotations

from pydantic import Field, model_validator
from typing import Any, Dict, TYPE_CHECKING

from .base import BaleObject
from .other_message import OtherMessage


class MessageViews(BaleObject):
    """
    Represents the view statistics of a message within Bale.

    This class holds a reference to the message itself and the number of times it has been viewed.
    The view count is extracted from a nested structure and represents a raw integer.

    Note:
    - The `views` field is unpacked from nested data during validation to simplify usage.
    """

    message: OtherMessage = Field(..., alias="1")
    """The original message object for which view statistics are recorded."""

    views: int = Field(..., alias="2")
    """The count of how many times the message has been viewed."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess input data before validation.

        The 'views' count arrives nested under key "2" and then key "1",
        so this method flattens it for easier access in the model.
        """
        data["2"] = data["2"]["1"]
        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: OtherMessage,
            views: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(message=message, views=views, **__pydantic_kwargs)
