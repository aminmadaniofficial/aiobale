from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject


class AuthBody(BaleObject):
    """
    Represents the authentication body used in the Bale API.

    This class is used to encapsulate the authentication state of a user.
    """

    authorized: int = Field(..., alias="1")
    """Indicates whether the user is authorized. 
    A value of 1 typically means the user is authorized, while 0 means not authorized."""

    ready: int = Field(..., alias="2")
    """Indicates whether the user is ready for further actions. 
    A value of 1 typically means ready, while 0 means not ready."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            authorized: int,
            ready: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(authorized=authorized, ready=ready, **__pydantic_kwargs)
