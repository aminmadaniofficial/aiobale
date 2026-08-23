from typing import Any, Dict
from pydantic import Field, model_validator
from typing import TYPE_CHECKING

from .base import BaleObject
from .int_bool import IntBool


class Permissions(BaleObject):
    """
    Represents a user's permissions within a group or channel context in Bale.

    Each permission is represented using `IntBool`, meaning the value is stored 
    as an integer (0 or 1) in the backend, but exposed as a boolean (`False` or `True`) in Python.

    Some fields are wrapped in nested dicts (e.g., {"1": true}) when their field number is greater than 10. 
    This is handled automatically in `model_dump()` and `fix_fields()`.
    """

    see_message: IntBool = Field(False, alias="1")
    """Permission to view messages."""

    delete_message: IntBool = Field(False, alias="2")
    """Permission to delete messages."""

    kick_user: IntBool = Field(False, alias="3")
    """Permission to remove users from the group."""

    pin_message: IntBool = Field(False, alias="4")
    """Permission to pin messages."""

    invite_user: IntBool = Field(False, alias="5")
    """Permission to invite users to the group."""

    add_admin: IntBool = Field(False, alias="6")
    """Permission to promote users to admin."""

    change_info: IntBool = Field(False, alias="7")
    """Permission to change group information."""

    send_message: IntBool = Field(False, alias="8")
    """Permission to send messages."""

    see_members: IntBool = Field(False, alias="9")
    """Permission to view the member list."""

    edit_message: IntBool = Field(False, alias="10")
    """Permission to edit sent messages."""

    send_media: IntBool = Field(False, alias="11")
    """Permission to send media (images, videos, etc.)."""

    send_gif_stickers: IntBool = Field(False, alias="12")
    """Permission to send GIFs and stickers."""

    reply_to_story: IntBool = Field(False, alias="13")
    """Permission to reply to stories."""

    forward_message_from: IntBool = Field(False, alias="14")
    """Permission to forward messages from others."""

    send_gift_packet: IntBool = Field(False, alias="15")
    """Permission to send gift packets."""

    start_call: IntBool = Field(False, alias="16")
    """Permission to initiate voice/video calls."""

    send_link_message: IntBool = Field(False, alias="17")
    """Permission to send messages that contain links."""

    send_forwarded_message: IntBool = Field(False, alias="18")
    """Permission to send forwarded messages."""

    add_story: IntBool = Field(False, alias="19")
    """Permission to add stories."""

    manage_call: IntBool = Field(False, alias="20")
    """Permission to manage ongoing calls."""

    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes incoming permission values.

        Some fields may come wrapped in a dict like {"1": true}. 
        This method extracts the inner value and ensures all falsy values are converted to `False`.
        """
        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]
            elif not value:
                data[key] = False
        return data

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Serializes the model, re-wrapping fields with key > 10 into {"1": value}
        to match Bale's expected data format.
        """
        data = super().model_dump(*args, **kwargs)
        for key, value in list(data.items()):
            try:
                int_key = int(key)
            except ValueError:
                continue

            if int_key > 10:
                data[key] = {"1": value}
        return data

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            see_message: IntBool = False,
            delete_message: IntBool = False,
            kick_user: IntBool = False,
            pin_message: IntBool = False,
            invite_user: IntBool = False,
            add_admin: IntBool = False,
            change_info: IntBool = False,
            send_message: IntBool = False,
            see_members: IntBool = False,
            edit_message: IntBool = False,
            send_media: IntBool = False,
            send_gif_stickers: IntBool = False,
            reply_to_story: IntBool = False,
            forward_message_from: IntBool = False,
            send_gift_packet: IntBool = False,
            start_call: IntBool = False,
            send_link_message: IntBool = False,
            send_forwarded_message: IntBool = False,
            add_story: IntBool = False,
            manage_call: IntBool = False,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                see_message=see_message,
                delete_message=delete_message,
                kick_user=kick_user,
                pin_message=pin_message,
                invite_user=invite_user,
                add_admin=add_admin,
                change_info=change_info,
                send_message=send_message,
                see_members=see_members,
                edit_message=edit_message,
                send_media=send_media,
                send_gif_stickers=send_gif_stickers,
                reply_to_story=reply_to_story,
                forward_message_from=forward_message_from,
                send_gift_packet=send_gift_packet,
                start_call=start_call,
                send_link_message=send_link_message,
                send_forwarded_message=send_forwarded_message,
                add_story=add_story,
                manage_call=manage_call,
                **__pydantic_kwargs
            )
