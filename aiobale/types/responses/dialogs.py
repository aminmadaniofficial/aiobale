from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING
from pydantic import Field, model_validator

from ..peer_data import PeerData
from ..base import BaleObject


class DialogResponse(BaleObject):
    """
    Represents a response containing a list of dialog peers.

    In Bale, dialogs refer to recent chats or active conversation threads. This class
    wraps the peer data for each dialog and ensures consistent structure even when
    the server returns a single object instead of a list.
    """

    dialogs: List[PeerData] = Field(default_factory=list, alias="3")
    """List of dialog peer data, representing recent conversations."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that the 'dialogs' field (alias '3') is always a list.

        Some server responses may return a single object instead of a list.
        This validator wraps such values in a list for consistency.
        """
        if "3" not in data:
            return data

        if not isinstance(data["3"], list):
            data["3"] = [data["3"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            dialogs: List[PeerData] = ...,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(dialogs=dialogs, **__pydantic_kwargs)
