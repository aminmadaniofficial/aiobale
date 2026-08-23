from typing import TYPE_CHECKING, Optional
from pydantic import Field

from .base import BaleObject
from .values import BoolValue


class Condition(BaleObject):
    """A class representing conditions for Bale bot actions.
    
    This class defines various permission and contact-related conditions
    that can be used to control bot behavior.
    """

    excepted_permissions: Optional[BoolValue] = Field(None, alias="1")
    """Whether specific permissions are excepted from the condition."""
    
    contacts: Optional[BoolValue] = Field(None, alias="2") 
    """Specifies if the condition applies to contacts."""

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            self,
            *,
            excepted_permissions: Optional[BoolValue] = None,
            contacts: Optional[BoolValue] = None,
            **kwargs
        ) -> None:
            super().__init__(
                excepted_permissions=excepted_permissions,
                contacts=contacts,
                **kwargs
            )
