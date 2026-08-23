from __future__ import annotations

from typing import List, Dict, Any, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..full_user import FullUser
from ..user import User


class FullUsersResponse(BaleObject):
    """
    Response model containing a list of detailed full user objects.

    Attributes:
        data (List[FullUser]): List of full user details returned by the server.
    """

    data: List[FullUser] = Field(default_factory=list, alias="1")
    """List of full user objects."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the 'data' field (alias '1') to always be a list.

        If the server returns a single FullUser object instead of a list,
        it is wrapped into a list for consistent processing.
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
            data: List[FullUser] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(data=data, **__pydantic_kwargs)


class UsersResponse(BaleObject):
    """
    Response model containing a list of basic user objects.

    Attributes:
        data (List[User]): List of user objects returned by the server.
    """

    data: List[User] = Field(default_factory=list, alias="1")
    """List of user objects."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the 'data' field (alias '1') to always be a list.

        If the server returns a single User object instead of a list,
        it is wrapped into a list for consistent processing.
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
            data: List[User] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(data=data, **__pydantic_kwargs)
