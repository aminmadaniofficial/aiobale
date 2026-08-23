from pydantic import Field
from typing import TYPE_CHECKING

from ..enums import SendType
from .base import BaleObject


class SendTypeModel(BaleObject):
    """
    Defines how a file should be sent in a Bale message.

    This model wraps a `SendType` enum that specifies the transmission mode — 
    for example, whether a file is sent as an image, document, video, etc.
    This helps the Bale client understand how to display or process the file.
    """

    type: SendType = Field(..., alias="1")
    """The desired send type (e.g., as image, document, video, etc.)."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            type: SendType,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(type=type, **__pydantic_kwargs)
