from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject


class UserBlocked(BaleObject):
    """
    Represents an event where a user has been blocked.

    Attributes:
        user_id (int): The unique identifier of the user who has been blocked.
    """
    user_id: int = Field(..., alias="1")
    """The unique identifier of the user who has been blocked."""
    
    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(user_id=user_id, **__pydantic_kwargs)

    
class UserUnblocked(BaleObject):
    """
    Represents an event where a user has been unblocked.

    Attributes:
        user_id (int): The unique identifier of the user who has been unblocked.
    """
    user_id: int = Field(..., alias="1")
    """The unique identifier of the user who has been unblocked."""
    
    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(user_id=user_id, **__pydantic_kwargs)
