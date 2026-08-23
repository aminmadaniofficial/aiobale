import os
import io
import mimetypes
from pathlib import Path
from typing import Union, Optional, NamedTuple

from ..utils import guess_mime_type


class FileData(NamedTuple):
    """
    Metadata container for file input.

    Attributes:
    - name (str): The file name (e.g., 'photo.jpg').
    - size (int): Size of the file in bytes.
    - mime_type (str): Detected or provided MIME type (e.g., 'image/jpeg').
    """
    name: str
    size: int
    mime_type: str


class FileInput:
    """
    A flexible abstraction for representing file input, either from a file path or from in-memory bytes.

    This class is used to standardize file handling, providing metadata extraction and async reading,
    regardless of whether the input is a file path or raw bytes. Useful for uploading files to APIs
    like Bale that expect both file content and metadata such as MIME type, size, and file name.

    Supported Inputs
    ================

    - File path (``str`` or ``Path``) – Reads directly from disk.
    - In-memory bytes (``bytes``) – Reads from provided byte content.

    Metadata Handling
    =================

    If ``name``, ``size``, or ``mime_type`` are not explicitly provided, the class will try to infer them:

    - For file paths: uses OS metadata and ``mimetypes.guess_type``.
    - For bytes: uses byte length and a custom MIME type detector (``guess_mime_type``), and creates a default name like ``upload.png``.

    Attributes
    ==========

    - ``info`` (``FileData``): A named tuple containing the resolved ``name``, ``size`` (in bytes), and ``mime_type``.

    Example
    =======

    .. code-block:: python

       file = FileInput("image.png")
       async for chunk in file.read():
           process(chunk)

       print(file.info.name, file.info.mime_type)

    Raises
    ======

    - ``TypeError``: If an unsupported type is passed to ``file`` (only ``str``, ``Path``, or ``bytes`` are allowed).
    """
    def __init__(
        self,
        file: Union[str, Path, bytes],
        *,
        name: Optional[str] = None,
        size: Optional[int] = None,
        mime_type: Optional[str] = None,
    ):
        if isinstance(file, (str, Path)):
            self._type = "path"
            self._path = Path(file)
        elif isinstance(file, bytes):
            self._type = "bytes"
            self._bytes = file
        else:
            raise TypeError("Unsupported file type")

        self.info = self._info(name=name, size=size, mime_type=mime_type)

    async def read(self, chunk_size: int = 4096):
        if self._type == "path":
            import aiofiles

            async with aiofiles.open(self._path, "rb") as f:
                while True:
                    chunk = await f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        elif self._type == "bytes":
            buf = io.BytesIO(self._bytes)
            while True:
                chunk = buf.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def _info(
        self, name: Optional[str], size: Optional[str], mime_type: Optional[str]
    ) -> FileData:
        if self._type == "path":
            path = self._path
            name = name or path.name
            size = size or os.path.getsize(path)
            mime_type = (
                mime_type
                or mimetypes.guess_type(path.name)[0]
                or "application/octet-stream"
            )
        elif self._type == "bytes":
            b = self._bytes
            size = size or len(b)
            mime_type = mime_type or guess_mime_type(b[:32])
            if not name:
                ext = mime_type.split("/")[-1]
                name = f"upload.{ext if ext.isalnum() else 'dat'}"

        return FileData(name=name, size=size, mime_type=mime_type)
    
    async def get_content(self) -> bytes:
        chunks = []
        async for chunk in self.read():
            chunks.append(chunk)
        return b''.join(chunks)
