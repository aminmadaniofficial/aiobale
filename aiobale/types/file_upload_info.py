from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaleObject


class FileUploadInfo(BaleObject):
    """
    Contains information required to upload a file to the Bale server.

    This includes a unique file ID, the upload URL, and the chunk size to be used 
    when uploading the file in multiple parts. Chunking is useful for uploading 
    large files efficiently and reliably.

    All values are provided by the server in preparation for a file upload session.
    """

    file_id: int = Field(..., alias="1")
    """Unique identifier for the file being uploaded."""

    url: str = Field(..., alias="2")
    """URL to which file chunks should be uploaded."""

    chunk_size: int = Field(262144, alias="4")
    """Recommended chunk size in bytes. Default is 262144 (256KB)."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            file_id: int,
            url: str,
            chunk_size: int = 262144,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(
                file_id=file_id,
                url=url,
                chunk_size=chunk_size,
                **__pydantic_kwargs,
            )
