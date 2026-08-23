from typing import TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject
from ..int_bool import IntBool
from .default import DefaultResponse


class NickNameAvailable(DefaultResponse):
    """
    Response model indicating if a nickname is available.

    Attributes:
        available (IntBool): Represents availability status as an integer from the server,
            but exposed as a boolean to the user. True if available, False otherwise.
    """

    available: IntBool = Field(False, alias="1")
    """Indicates whether the requested nickname is available."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            available: IntBool = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(available=available, **__pydantic_kwargs)
