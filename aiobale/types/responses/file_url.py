from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING
from pydantic import Field, model_validator

from ..base import BaleObject
from ..file_url import FileURL


class FileURLResponse(BaleObject):
    """
    Response containing a list of file URLs.

    This model wraps a list of FileURL objects typically returned from
    an API call that provides downloadable or accessible file links.

    The validator ensures that the 'file_urls' field (alias '1') is always
    a list, converting single item responses into a list for consistency.
    """

    file_urls: List[FileURL] = Field(default_factory=list, alias="1")
    """List of file URLs provided by the server."""

    @model_validator(mode="before")
    @classmethod
    def validate_list(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the 'file_urls' field to always be a list.

        Sometimes the API returns a single FileURL object instead of a list.
        This method wraps such cases in a list for consistent processing.
        """
        if "1" not in data:
            return data

        if not isinstance(data["1"], list):
            data["1"] = [data["1"]]

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            file_urls: List[FileURL] = ...,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(file_urls=file_urls, **__pydantic_kwargs)
