from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from pydantic import Field

from ..base import BaleObject
from ..full_group import FullGroup


class FullGroupResponse(BaleObject):
    """
    Response containing the full details of a group.

    This object wraps the `FullGroup` data which includes comprehensive
    information about a group in the Bale messaging platform.
    """

    fullgroup: Optional[FullGroup] = Field(None, alias="1")
    """The full group details; may be None if not provided by the server."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            fullgroup: Optional[FullGroup] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(fullgroup=fullgroup, **__pydantic_kwargs)
