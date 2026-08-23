from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, Dict

from .base import BaleObject


class FileURL(BaleObject):
    """
    Represents a downloadable file URL along with metadata.

    This object is returned when requesting a file from the server.
    It includes the actual URL, the file ID it's linked to, a timeout for validity, 
    and the chunk size to be used for segmented downloads.

    Note: All timestamps and durations (like timeout) are in milliseconds.
    """

    file_id: int = Field(..., alias="1")
    """Unique identifier for the file."""

    url: str = Field(..., alias="2")
    """The temporary download URL of the file."""

    timeout: int = Field(..., alias="3")
    """Validity duration of the URL in milliseconds."""

    chunk_size: int = Field(65536, alias="7")
    """Recommended chunk size (in bytes) for downloading the file in parts."""

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the `chunk_size` field if it's wrapped as a value object.

        Bale sometimes wraps primitives like chunk size inside a dict: {"1": value},
        so we unwrap it here before model validation.
        """
        if "7" in data and isinstance(data["7"], dict) and "1" in data["7"]:
            data["7"] = data["7"]["1"]
        return data

    if TYPE_CHECKING:
        # This __init__ is only for IDE autocomplete and type checking purposes.
        # It is not executed at runtime.
        def __init__(
            __pydantic__self__,
            *,
            file_id: int,
            url: str,
            timeout: int,
            chunk_size: int,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                file_id=file_id,
                url=url,
                timeout=timeout,
                chunk_size=chunk_size,
                **__pydantic_kwargs,
            )
