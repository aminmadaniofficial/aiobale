from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject
from .values import StringValue


class ContactData(BaleObject):
    """Represents contact data in Bale messenger.
    
    This class contains essential information about a contact,
    including their phone number and name.
    """

    phone_number: int = Field(..., alias="1")
    """The contact's phone number in international format"""
    
    name: StringValue = Field(..., alias="2")
    """The contact's display name"""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            phone_number: int,
            name: StringValue,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                phone_number=phone_number,
                name=name,
                **__pydantic_kwargs
            )
