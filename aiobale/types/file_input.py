import io
import os
import mimetypes
from pathlib import Path
from typing import Union, Optional, NamedTuple, Any

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
    A flexible abstraction for representing file input, either from a file path,
    in-memory bytes, or a file-like stream (io.IOBase / io.BytesIO).

    This class standardizes file handling across all aiobale sending and uploading methods.
    """

    def __init__(
        self,
        file: Union[str, Path, bytes, io.IOBase],
        *,
        name: Optional[str] = None,
        size: Optional[int] = None,
        mime_type: Optional[str] = None,
    ):
        if isinstance(file, (str, Path)):
            self._type = "path"
            self._path = Path(file)
            if not self._path.exists():
                raise FileNotFoundError(f"File not found: {self._path}")
        elif isinstance(file, bytes):
            self._type = "bytes"
            self._bytes = file
        elif isinstance(file, io.IOBase):
            self._type = "io"
            self._io = file
        else:
            raise TypeError(
                f"Unsupported file type: {type(file).__name__}. Expected str, Path, bytes, or io.IOBase."
            )

        self.info = self._info(name=name, size=size, mime_type=mime_type)

    @classmethod
    def ensure(cls, file: Any, **kwargs: Any) -> Any:
        """
        Converts file path, bytes, or stream into a FileInput instance if needed.
        If already a FileInput, FileDetails, or DocumentMessage, returns as is.
        """
        if isinstance(file, (str, Path, bytes, io.IOBase)):
            return cls(file, **kwargs)
        return file

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
        elif self._type == "io":
            # For stream/file-like object
            if hasattr(self._io, "seekable") and self._io.seekable():
                self._io.seek(0)
            while True:
                chunk = self._io.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def _info(
        self,
        name: Optional[str],
        size: Optional[int],
        mime_type: Optional[str],
    ) -> FileData:
        if self._type == "path":
            path = self._path
            resolved_name = name or path.name
            resolved_size = size or os.path.getsize(path)
            resolved_mime = (
                mime_type
                or mimetypes.guess_type(path.name)[0]
                or "application/octet-stream"
            )
        elif self._type == "bytes":
            b = self._bytes
            resolved_size = size or len(b)
            resolved_mime = mime_type or guess_mime_type(b[:64])
            if not name:
                ext = resolved_mime.split("/")[-1]
                resolved_name = f"upload.{ext if ext.isalnum() else 'dat'}"
            else:
                resolved_name = name
        elif self._type == "io":
            resolved_name = name or getattr(self._io, "name", "upload.dat")
            if isinstance(resolved_name, (Path, str)):
                resolved_name = Path(resolved_name).name

            if size is not None:
                resolved_size = size
            elif isinstance(self._io, io.BytesIO):
                resolved_size = len(self._io.getvalue())
            elif hasattr(self._io, "seekable") and self._io.seekable():
                curr = self._io.tell()
                self._io.seek(0, io.SEEK_END)
                resolved_size = self._io.tell()
                self._io.seek(curr)
            else:
                resolved_size = 0

            if mime_type:
                resolved_mime = mime_type
            elif isinstance(self._io, io.BytesIO):
                resolved_mime = guess_mime_type(self._io.getvalue()[:64])
            else:
                resolved_mime = mimetypes.guess_type(str(resolved_name))[0] or "application/octet-stream"

        return FileData(name=str(resolved_name), size=int(resolved_size), mime_type=str(resolved_mime))

    async def get_content(self) -> bytes:
        chunks = []
        async for chunk in self.read():
            chunks.append(chunk)
        return b''.join(chunks)
