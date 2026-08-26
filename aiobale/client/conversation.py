from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, Optional, Union
from ..enums import ChatType
from ..types import InlineKeyboardMarkup, Message

if TYPE_CHECKING:
    from .client import Client


class Conversation:
    """
    Asynchronous Context Manager for linear, interactive conversations with a user or chat.
    
    Example:
        ```python
        async with client.conversation(chat_id=123456) as conv:
            await conv.send_message("Please enter your name:")
            name_msg = await conv.get_response(timeout=60)
            print(f"User name: {name_msg.text}")
        ```
    """

    def __init__(
        self,
        client: Client,
        chat_id: int,
        chat_type: ChatType = ChatType.PRIVATE,
        timeout: Optional[float] = None,
    ) -> None:
        self.client = client
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.timeout = timeout
        self._queue: asyncio.Queue[Message] = asyncio.Queue()
        self._closed: bool = False

    async def __aenter__(self) -> Conversation:
        self.client._register_conversation(self)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._closed = True
        self.client._unregister_conversation(self)

    def is_closed(self) -> bool:
        return self._closed

    def put_message(self, message: Message) -> None:
        if not self._closed:
            self._queue.put_nowait(message)

    async def get_response(self, timeout: Optional[float] = None) -> Message:
        """
        Awaits and returns the next incoming message in this conversation.
        """
        if self._closed:
            raise RuntimeError("Conversation is already closed.")
        effective_timeout = timeout if timeout is not None else self.timeout
        if effective_timeout is not None:
            return await asyncio.wait_for(self._queue.get(), timeout=effective_timeout)
        return await self._queue.get()

    async def send_message(
        self,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        message_id: Optional[int] = None,
    ) -> Message:
        return await self.client.send_message(
            text=text,
            chat_id=self.chat_id,
            chat_type=self.chat_type,
            reply_markup=reply_markup,
            message_id=message_id,
        )

    async def send_photo(
        self,
        photo: Any,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        message_id: Optional[int] = None,
    ) -> Message:
        return await self.client.send_photo(
            photo=photo,
            chat_id=self.chat_id,
            chat_type=self.chat_type,
            caption=caption,
            reply_markup=reply_markup,
            message_id=message_id,
        )

    async def send_document(
        self,
        file: Any,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        message_id: Optional[int] = None,
    ) -> Message:
        return await self.client.send_document(
            file=file,
            chat_id=self.chat_id,
            chat_type=self.chat_type,
            caption=caption,
            reply_markup=reply_markup,
            message_id=message_id,
        )
