from pydantic import Field
from typing import TYPE_CHECKING, List, Optional

from ...types import ShortPeer, StringValue
from ...types.responses import GroupCreatedResponse
from ...enums import Services, GroupType, Restriction
from ..base import BaleMethod


class CreateGroup(BaleMethod):
    """
    Creates a new group with specified parameters.

    Returns:
        aiobale.types.responses.GroupCreatedResponse: The response containing details of the created group.
    """

    __service__ = Services.GROUPS.value
    __method__ = "CreateGroup"

    __returning__ = GroupCreatedResponse

    random_id: int = Field(..., alias="1")
    """
    A unique random identifier for the group creation request. Used to ensure idempotency and avoid duplicate group creation.
    """

    title: str = Field(..., alias="2")
    """
    The display name or title of the group to be created.
    """

    users: Optional[List[ShortPeer]] = Field(None, alias="3")
    """
    Optional list of users (peers) to be added as initial members of the group.
    """

    group_type: GroupType = Field(GroupType.GROUP, alias="6")
    """
    The type of group to create (e.g., regular group, supergroup). Defaults to a standard group.
    """

    username: Optional[StringValue] = Field(None, alias="8")
    """
    Optional username for the group, allowing it to be publicly accessible or searchable.
    """

    restriction: Restriction = Field(Restriction.PRIVATE, alias="9")
    """
    Restriction level for the group, such as private or public. Determines group visibility and join permissions.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            random_id: int,
            title: str,
            users: Optional[List[ShortPeer]],
            group_type: GroupType = GroupType.GROUP,
            username: Optional[StringValue] = None,
            restriction: Restriction = Restriction.PRIVATE,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                random_id=random_id,
                title=title,
                users=users,
                group_type=group_type,
                username=username,
                restriction=restriction,
                **__pydantic_kwargs
            )
