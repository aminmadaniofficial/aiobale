from __future__ import annotations

from typing import List, Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from .default import DefaultResponse
from ...types import InfoPeer


class ContactsResponse(DefaultResponse):
    """
    Response class for contact list requests.

    This response contains a list of peers (users, bots, channels, etc.)
    that are returned from a contacts-related API call. The peer information
    is normalized in case the server returns a single object instead of a list.
    """

    peers: List[InfoPeer] = Field(..., alias="4")
    """List of contact peers returned from the server."""

    @model_validator(mode="before")
    @classmethod
    def add_message(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures the 'peers' field (alias '4') is always a list.

        Some server responses may return a single object instead of a list.
        This validator converts such cases into a proper list for consistency.
        """
        if "4" not in data:
            data["4"] = []
        elif not isinstance(data["4"], list):
            data["4"] = [data["4"]]
        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            peers: List[InfoPeer],
            **__pydantic_kwargs
        ) -> None:
            super().__init__(peers=peers, **__pydantic_kwargs)
