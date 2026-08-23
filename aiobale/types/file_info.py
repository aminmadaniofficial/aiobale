from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject
from .values import IntValue


class FileInfo(BaleObject):
    """
    Represents metadata for a file in Bale.

    This includes the file's unique ID, access hash (used for secure file access),
    and a version indicator for the file's storage format or protocol version.

    The `file_storage_version` defaults to 1 and can be used for handling different
    storage strategies or migration logic in the future.
    """

    file_id: int = Field(..., alias="1")
    """Unique identifier for the file."""

    access_hash: int = Field(..., alias="2")
    """Access hash used to securely access or validate the file."""

    file_storage_version: IntValue = Field(
        default_factory=lambda: IntValue(value=1),
        alias="3"
    )
    """Version of the file storage format. Defaults to 1."""

    if TYPE_CHECKING:
        # This __init__ is only for IDE autocomplete and type checking purposes.
        # It is not executed at runtime.
        def __init__(
            __pydantic__self__,
            *,
            file_id: int,
            access_hash: int,
            file_storage_version: IntValue = IntValue(value=1),
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                file_id=file_id,
                access_hash=access_hash,
                file_storage_version=file_storage_version,
                **__pydantic_kwargs,
            )
