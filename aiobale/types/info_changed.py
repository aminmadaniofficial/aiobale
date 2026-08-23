from pydantic import Field, model_validator
from typing import Any, Dict, Optional, TYPE_CHECKING

from .base import BaleObject


class UsernameChanged(BaleObject):
    """
    Represents an update event where a user's username has changed.

    Attributes:
        user_id: The unique identifier of the user whose username changed.
        username: The new username of the user, if available.
    """

    user_id: int = Field(..., alias="1")
    """The ID of the user who changed their username."""

    username: Optional[str] = Field(None, alias="2")
    """The updated username as a string, or None if not provided."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-processes incoming raw data before validation.

        The 'username' field arrives nested as data["2"]["1"], 
        so this method extracts the actual string username to simplify model parsing.

        Args:
            data: Raw data dictionary from the update event.

        Returns:
            Modified data dictionary with the 'username' field flattened.
        """
        # Only adjust 'username' if it exists in the input data
        if "2" in data and isinstance(data["2"], dict) and "1" in data["2"]:
            data["2"] = data["2"]["1"]

        return data

    if TYPE_CHECKING:
        # For type checking and IDE support only; not part of runtime
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            username: Optional[str] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(user_id=user_id, username=username, **__pydantic_kwargs)


class AboutChanged(BaleObject):
    """
    Represents an update event where a user's 'about' or bio text has changed.

    Attributes:
        user_id: The unique identifier of the user whose 'about' was changed.
        about: The new 'about' text of the user.
    """

    user_id: int = Field(..., alias="1")
    """The ID of the user who updated their 'about' text."""

    about: Optional[str] = Field(None, alias="2")
    """The updated 'about' or bio string."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-processes incoming raw data before validation.

        The 'about' field is nested as data["2"]["1"], so this method extracts 
        the string to simplify model parsing.

        Args:
            data: Raw data dictionary from the update event.

        Returns:
            Modified data dictionary with the 'about' field flattened.
        """
        # Defensive check: only flatten if expected structure exists
        if "2" in data and isinstance(data["2"], dict) and "1" in data["2"]:
            data["2"] = data["2"]["1"]

        return data

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            user_id: int,
            about: str,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(user_id=user_id, about=about, **__pydantic_kwargs)
