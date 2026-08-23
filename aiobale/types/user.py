from pydantic import Field, model_validator
from typing import Dict, Any, Optional, TYPE_CHECKING

from .base import BaleObject
from .int_bool import IntBool
from .full_user import ExInfo
from .values import StringValue


class UserAuth(BaleObject):
    """
    Contains basic authentication-related information of a Bale user.

    Typically received right after login or loaded from session data,
    this includes user ID, access hash for authorization, display name,
    and optionally a wrapped username string.
    """

    id: int = Field(..., alias="1")
    """Unique identifier of the user."""

    access_hash: int = Field(-1, alias="2")
    """Access hash used for secure identification and authorization."""

    name: str = Field(..., alias="3")
    """Display name of the user."""

    username: Optional[StringValue] = Field(None, alias="9")
    """Optional username wrapped in a `StringValue` type, which can hold additional metadata."""


    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            access_hash: int,
            name: str,
            username: Optional[StringValue] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(id=id, access_hash=access_hash, name=name, username=username, **__pydantic_kwargs)


class User(BaleObject):
    """
    Detailed information about a Bale user, including profile and status data.

    This data is provided post-login or loaded from session and contains
    both public and internal user fields.
    
    All timestamp fields (like `created_at`) are in milliseconds since epoch.
    """

    id: int = Field(..., alias="1")
    """Unique user ID."""

    access_hash: int = Field(..., alias="2")
    """Access hash used for secure identification and authorization."""

    name: str = Field(..., alias="3")
    """Primary display name of the user."""

    local_name: Optional[str] = Field(None, alias="4")
    """Localized name or nickname, if available."""

    sex: Optional[int] = Field(None, alias="5")
    """User's sex as an integer code (e.g., 0 = unknown, 1 = male, 2 = female)."""

    is_bot: IntBool = Field(False, alias="7")
    """Flag indicating if the user is a bot account."""

    username: Optional[str] = Field(None, alias="9")
    """Username as a simple string, if set."""

    is_deleted: IntBool = Field(False, alias="16")
    """Flag indicating if the user account is deleted."""

    created_at: int = Field(..., alias="19")
    """Account creation timestamp in milliseconds since epoch."""

    ex_info: ExInfo = Field(..., alias="20")
    """Extended user information, such as profile photos, status, or additional metadata."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess raw input data before validation.

        This method unwraps fields that are encoded as single-key dictionaries
        (e.g., {"1": value}) into their inner values for easier use.

        It also removes empty or falsy fields except for the mandatory `ex_info` (key "20").
        """
        for key in list(data.keys()):
            value = data[key]

            if key == "20":
                # Keep ex_info as is (usually a nested dict)
                continue

            elif isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif not value:
                # Remove empty or falsy values except ex_info
                data.pop(key)

        return data

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            access_hash: int,
            name: str,
            local_name: Optional[str] = None,
            sex: Optional[int] = None,
            is_bot: IntBool = False,
            username: Optional[str] = None,
            is_deleted: IntBool = False,
            created_at: int = ...,
            ex_info: ExInfo = ...,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                id=id,
                access_hash=access_hash,
                name=name,
                local_name=local_name,
                sex=sex,
                is_bot=is_bot,
                username=username,
                is_deleted=is_deleted,
                created_at=created_at,
                ex_info=ex_info,
                **__pydantic_kwargs,
            )
