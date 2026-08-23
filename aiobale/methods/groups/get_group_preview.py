from pydantic import Field
from typing import TYPE_CHECKING

from ...types.responses import FullGroupResponse
from ...enums import Services
from ..base import BaleMethod


class GetGroupPreview(BaleMethod):
    """
    Retrieves a preview of a group based on the provided token.

    Returns:
        aiobale.types.responses.FullGroupResponse: The response containing the group preview details.
    """

    __service__ = Services.GROUPS.value
    __method__ = "GetGroupPreview"

    __returning__ = FullGroupResponse

    token: str = Field(..., alias="1")
    """
    The unique token identifying the group for which the preview is requested.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(__pydantic__self__, *, token: str, **__pydantic_kwargs) -> None:
            super().__init__(token=token, **__pydantic_kwargs)
