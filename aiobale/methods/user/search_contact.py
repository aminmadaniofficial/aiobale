from pydantic import Field
from typing import TYPE_CHECKING, Any

from ...types.responses import ContactResponse
from ...enums import Services
from ..base import BaleMethod


class SearchContact(BaleMethod):
    """
    Searches for a contact using a given query string.

    Returns:
        aiobale.types.responses.ContactResponse: The response containing matching contact information.
    """

    __service__ = Services.USER.value
    __method__ = "SearchContacts"

    __returning__ = ContactResponse

    request: str = Field(..., alias="1")
    """
    The search query used to find the contact (e.g., phone number, username, or name).
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, request: str, **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(request=request, **__pydantic_kwargs)
