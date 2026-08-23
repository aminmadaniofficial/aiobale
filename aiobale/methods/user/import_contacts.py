from pydantic import Field
from typing import TYPE_CHECKING, Any, List

from ...types.responses import ContactsResponse
from ...types import ContactData
from ...enums import Services
from ..base import BaleMethod


class ImportContacts(BaleMethod):
    """
    Imports a list of contacts into the user's account.

    Returns:
        aiobale.types.responses.ContactsResponse: The response containing the imported contacts data.
    """

    __service__ = Services.USER.value
    __method__ = "ImportContacts"

    __returning__ = ContactsResponse

    phones: List[ContactData] = Field(..., alias="1")
    """
    A list of contact data to be imported.
    Each contact is represented as a `ContactData` object.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, phones: List[ContactData], **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(phones=phones, **__pydantic_kwargs)
