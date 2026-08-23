from typing import Any, Dict, List, Optional, TYPE_CHECKING
from pydantic import Field, model_validator

from ..enums import ChatType, PrivacyMode
from .int_bool import IntBool
from .base import BaleObject
from .ext import ExtKeyValue


class ExInfo(BaleObject):
    """
    Contains extended metadata about a peer, such as its type and verification status.
    
    Typically used in `FullUser` and `FullGroup` to describe whether the user/group/channel is verified.
    """

    expeer_type: ChatType = Field(..., alias="1")
    """The type of peer (e.g., User, Group, Channel)."""

    identified: IntBool = Field(False, alias="2")
    """Indicates if the peer is verified (has the blue badge)."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            expeer_type: ChatType,
            identified: IntBool = False,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(expeer_type=expeer_type, identified=identified, **__pydantic_kwargs)


class ContactInfo(BaleObject):
    """
    Represents an optional contact entry (like phone or username) attached to a user.
    
    This is used to show additional context about how this user is saved in your contact list.
    """

    value: Optional[int] = Field(None, alias="3")
    """The numeric value (e.g., phone number ID) associated with the contact field."""

    title: Optional[str] = Field(None, alias="4")
    """The label or title of this contact field (e.g., 'mobile', 'home')."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Fix values that are improperly wrapped inside {"1": value}
        for key, value in list(data.items()):
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]
        return data

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            value: Optional[int] = None,
            title: Optional[str] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(value=value, title=title, **__pydantic_kwargs)


class FullUser(BaleObject):
    """
    Represents a full user profile with metadata, privacy settings, and extended info.

    This model combines standard user attributes (like about and timezone) with
    richer information like bot commands, verification status, and privacy mode.
    It also includes data clean-up logic to normalize and sanitize inconsistent backend formats.
    """

    id: int = Field(..., alias="1")
    """Unique numeric ID of the user."""

    contact_info: Optional[ContactInfo] = Field(None, alias="2")
    """Optional contact metadata (e.g., labels, saved numbers)."""

    about: Optional[str] = Field(None, alias="3")
    """User's 'about' section (biography or status)."""

    languages: Optional[List[str]] = Field(None, alias="4")
    """List of language codes that the user prefers (e.g., ['fa', 'en'])."""

    timezone: Optional[str] = Field(None, alias="5")
    """Timezone string of the user (e.g., 'Asia/Tehran')."""

    bot_commands: Optional[List[ExtKeyValue]] = Field(None, alias="6")
    """List of bot commands available to this user if they are a bot."""

    is_blocked: IntBool = Field(False, alias="8")
    """True if the current client has blocked this user."""

    ex_info: ExInfo = Field(..., alias="9")
    """Extended metadata about the user (e.g., peer type, verification status)."""

    is_deleted: IntBool = Field(False, alias="12")
    """True if the user account is deleted."""

    is_contact: IntBool = Field(False, alias="13")
    """True if the user is in the current client's contact list."""

    created_at: int = Field(..., alias="15")
    """Unix timestamp of when the user account was created."""

    privacy_mode: PrivacyMode = Field(..., alias="16")
    """User's privacy mode (e.g., who can see their phone number, status, etc.)."""

    allowed_invite: IntBool = Field(False, alias="17")
    """True if this user allows being invited to groups/channels."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Fix improperly nested fields, remove falsy fields, and normalize structure
        for key, value in list(data.items()):
            if key == "9":  # ex_info must remain as is
                continue

            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]

            elif key == "4" and not isinstance(value, list):
                data[key] = [value]

            elif not value:
                data.pop(key)

        return data

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            id: int,
            contact_info: Optional[ContactInfo] = None,
            about: Optional[str] = None,
            languages: Optional[List[str]] = None,
            timezone: Optional[str] = None,
            bot_commands: Optional[List[ExtKeyValue]] = None,
            is_blocked: IntBool = False,
            ex_info: ExInfo,
            is_deleted: IntBool = False,
            is_contact: IntBool = False,
            created_at: int,
            privacy_mode: PrivacyMode,
            allowed_invite: IntBool = False,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                id=id,
                contact_info=contact_info,
                about=about,
                languages=languages,
                timezone=timezone,
                bot_commands=bot_commands,
                is_blocked=is_blocked,
                ex_info=ex_info,
                is_deleted=is_deleted,
                is_contact=is_contact,
                created_at=created_at,
                privacy_mode=privacy_mode,
                allowed_invite=allowed_invite,
                **__pydantic_kwargs
            )
