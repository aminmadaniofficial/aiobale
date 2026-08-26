import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

from aiobale import Client, Conversation
from aiobale.types import Message, Chat, MessageContent, TextMessage, DocumentMessage, UpdateBody, Update
from aiobale.enums import ChatType, ListLoadMode
from aiobale.filters import IsMedia, TextEquals, TextContains, TextStartsWith, TextEndsWith


def make_sample_message(message_id: int, date: int, text: str = "Hello", chat_id: int = 123456) -> Message:
    return Message.model_validate(
        {
            "1": {"1": 1, "2": chat_id},
            "2": 999,
            "3": date,
            "4": message_id,
            "5": {"text": {"1": text}},
        }
    )


@pytest.mark.asyncio
async def test_iter_messages_pagination():
    mock_client = MagicMock(spec=Client)

    # Batch 1 (messages 3, 2)
    batch_1 = [
        make_sample_message(3, 3000, "Msg 3"),
        make_sample_message(2, 2000, "Msg 2"),
    ]
    # Batch 2 (message 1)
    batch_2 = [
        make_sample_message(1, 1000, "Msg 1"),
    ]

    mock_client.load_history = AsyncMock(side_effect=[batch_1, batch_2, []])

    # Test iter_messages generator directly using the bound method
    iter_gen = Client.iter_messages(
        mock_client,
        chat_id=123456,
        chat_type=ChatType.PRIVATE,
        limit=5,
        chunk_size=2,
    )

    collected = []
    async for msg in iter_gen:
        collected.append(msg)

    assert len(collected) == 3
    assert [m.message_id for m in collected] == [3, 2, 1]


@pytest.mark.asyncio
async def test_conversation_context_and_queue():
    mock_client = MagicMock(spec=Client)
    mock_client._conversations = {}
    mock_client._register_conversation = lambda conv: mock_client._conversations.update({conv.chat_id: conv})
    mock_client._unregister_conversation = lambda conv: mock_client._conversations.pop(conv.chat_id, None)
    mock_client.send_message = AsyncMock(return_value=make_sample_message(100, 1000, "Prompt"))

    async with Conversation(mock_client, chat_id=777) as conv:
        assert 777 in mock_client._conversations
        assert conv.is_closed() is False

        # Sending prompt
        sent = await conv.send_message("What is your name?")
        assert sent.text == "Prompt"

        # Simulate incoming update delivering to conversation queue
        incoming_msg = make_sample_message(101, 1001, "Ali", chat_id=777)
        conv.put_message(incoming_msg)

        resp = await conv.get_response(timeout=1.0)
        assert resp.text == "Ali"
        assert resp.message_id == 101

    assert 777 not in mock_client._conversations
    assert conv.is_closed() is True


@pytest.mark.asyncio
async def test_text_and_media_filters():
    text_msg = make_sample_message(1, 100, "Start Bot Registration")
    media_msg = Message.model_validate(
        {
            "1": {"1": 1, "2": 123},
            "2": 999,
            "3": 100,
            "4": 2,
            "5": {
                "document": {
                    "file_id": 11,
                    "access_hash": 22,
                    "size": 100,
                    "name": "photo.jpg",
                    "mime_type": "image/jpeg",
                }
            },
        }
    )

    # Text filters
    f_eq = TextEquals("start bot registration")
    assert await f_eq(text_msg) is True

    f_contains = TextContains("Bot")
    assert await f_contains(text_msg) is True

    f_starts = TextStartsWith("Start")
    assert await f_starts(text_msg) is True

    f_ends = TextEndsWith("Registration")
    assert await f_ends(text_msg) is True

    # Media filter
    f_media = IsMedia()
    assert await f_media(media_msg) is True
    assert await f_media(text_msg) is False
