from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ...types import ShortPeer, Condition, StringValue
from ...types.responses import MembersResponse
from ...enums import Services
from ..base import BaleMethod


class LoadMembers(BaleMethod):
    """
    Loads members of a group with optional filtering conditions.
    
    Returns:
        aiobale.types.responses.MembersResponse: The response containing the list of group members.
    """

    __service__ = Services.GROUPS.value
    __method__ = "LoadMembers"

    __returning__ = MembersResponse

    group: ShortPeer = Field(..., alias="1")
    """
    The group for which members are being loaded.
    """

    limit: int = Field(..., alias="2")
    """
    The maximum number of members to retrieve.
    """

    next_offset: Optional[StringValue] = Field(None, alias="3")
    """
    The pagination offset for retrieving the next set of members.
    """

    condition: Optional[Condition] = Field(None, alias="4")
    """
    Optional filtering condition to apply when loading members.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            group: ShortPeer,
            limit: int,
            next_offset: int,
            condition: Optional[Condition] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                group=group,
                limit=limit,
                next=next_offset,
                condition=condition,
                **__pydantic_kwargs
            )
