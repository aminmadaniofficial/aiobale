from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import DialogResponse
from ...enums import Services
from ..base import BaleMethod


class LoadDialogs(BaleMethod):
    """
    Loads a list of dialogs (chats, groups, or channels) with optional filters.
    
    Returns:
        aiobale.types.responses.DialogResponse: The response containing the list of dialogs.
    """

    __service__ = Services.MESSAGING.value
    __method__ = "LoadDialogs"

    __returning__ = DialogResponse

    offset_date: int = Field(..., alias="1")
    """
    The starting point for loading dialogs, specified as a timestamp.
    """

    limit: int = Field(..., alias="2")
    """
    The maximum number of dialogs to retrieve.
    """

    exclude_pinned: bool = Field(..., alias="5")
    """
    Whether to exclude pinned dialogs from the results.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            offset_date: int,
            limit: int,
            exclude_pinned: bool,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                offset_date=offset_date,
                limit=limit,
                exclude_pinned=exclude_pinned,
                **__pydantic_kwargs
            )
