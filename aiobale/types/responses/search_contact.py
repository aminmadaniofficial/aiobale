from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from pydantic import Field

from ..base import BaleObject
from ..info_peer import InfoPeer


class ContactResponse(BaleObject):
    """
    Response model representing a contact search result.

    Attributes:
        user (Optional[InfoPeer]): If the found contact is a user or a bot,
            its information will be stored here.
        group (Optional[InfoPeer]): If the found contact is a channel or group,
            its information will be stored here.
    """

    user: Optional[InfoPeer] = Field(None, alias="2")
    """Contains user or bot information if the contact is of that type."""

    group: Optional[InfoPeer] = Field(None, alias="5")
    """Contains channel or group information if the contact is of that type."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            user: Optional[InfoPeer] = None,
            chat: Optional[InfoPeer] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(user=user, chat=chat, **__pydantic_kwargs)
