from typing import Any, Dict, TYPE_CHECKING
from pydantic import Field, model_validator

from .base import BaleObject

class BanData(BaleObject):
    """
    Represents data related to a ban event in the system.
    This class is used to encapsulate information about a ban, including
    the ID of the banned entity and the ID of the banner (the entity that
    initiated the ban).
    """
    banned_id: int = Field(..., alias="1")
    """The ID of the entity that has been banned. This is a required field."""
    banner_id: int = Field(..., alias="2")
    """The ID of the entity that initiated the ban. This is a required field."""
    
    @model_validator(mode="before")
    @classmethod
    def fix_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        A validator to preprocess the input data before model validation.
        This method ensures that nested dictionaries with a single key "1"
        are flattened to their value. This is useful for handling specific
        data structures that may be returned by external systems.
        """
        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, dict) and len(value) == 1 and "1" in value:
                data[key] = value["1"]
        return data
    
    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            banned_id: int,
            banner_id: int,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(banned_id=banned_id, banner_id=banner_id, **__pydantic_kwargs)
