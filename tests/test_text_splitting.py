import io
import pytest
from unittest.mock import AsyncMock, MagicMock

from aiobale.utils import smart_split_text
from aiobale import Client
from aiobale.types import Message, Chat, MessageContent, TextMessage
from aiobale.enums import ChatType


def test_smart_split_text_short():
    res = smart_split_text("Short text", max_length=100)
    assert res == ["Short text"]


def test_smart_split_text_empty():
    assert smart_split_text("", max_length=100) == [""]


def test_smart_split_text_newline_boundary():
    line1 = "Line 1: " + "a" * 30
    line2 = "Line 2: " + "b" * 30
    text = f"{line1}\n{line2}"

    # Split with max_length=45 (should split at \n between line1 and line2)
    chunks = smart_split_text(text, max_length=45)
    assert len(chunks) == 2
    assert chunks[0] == line1
    assert chunks[1] == line2


def test_smart_split_text_space_boundary():
    word1 = "Hello"
    word2 = "World"
    word3 = "Bale"
    text = f"{word1} {word2} {word3}"

    chunks = smart_split_text(text, max_length=12)
    assert len(chunks) == 2
    assert chunks[0] == "Hello World"
    assert chunks[1] == "Bale"


def test_smart_split_text_hard_cut():
    huge_word = "X" * 150
    chunks = smart_split_text(huge_word, max_length=50)
    assert len(chunks) == 3
    assert all(len(c) <= 50 for c in chunks)
    assert "".join(chunks) == huge_word


@pytest.mark.asyncio
async def test_client_send_message_auto_split():
    mock_client = MagicMock(spec=Client)
    sent_msgs = []

    async def fake_send_message(text, chat_id, chat_type, reply_markup=None, reply_to=None, auto_split=False, max_split_length=4000, **kwargs):
        if auto_split and len(text) > max_split_length:
            chunks = smart_split_text(text, max_length=max_split_length)
            results = []
            for i, chunk in enumerate(chunks):
                chunk_reply = reply_to if i == 0 else None
                chunk_markup = reply_markup if i == len(chunks) - 1 else None
                msg = await fake_send_message(
                    text=chunk,
                    chat_id=chat_id,
                    chat_type=chat_type,
                    reply_markup=chunk_markup,
                    reply_to=chunk_reply,
                    auto_split=False,
                )
                results.append(msg)
            return results

        m = Message.model_validate(
            {
                "1": {"1": 1, "2": chat_id},
                "2": 999,
                "3": 1700000000,
                "4": len(sent_msgs) + 1,
                "5": {"text": {"1": text}},
            }
        )
        sent_msgs.append(m)
        return m

    mock_client.send_message = fake_send_message

    long_text = "Paragraph 1: " + ("Hello Bale! " * 50) + "\nParagraph 2: " + ("Second part text " * 50)
    
    # Test auto_split with limit of 300 chars
    res = await mock_client.send_message(
        long_text,
        chat_id=12345,
        chat_type=ChatType.PRIVATE,
        auto_split=True,
        max_split_length=300,
    )

    assert isinstance(res, list)
    assert len(res) > 1
    for msg in res:
        assert isinstance(msg, Message)
        assert len(msg.text) <= 300


@pytest.mark.asyncio
async def test_message_reply_auto_split_integration():
    mock_client = MagicMock(spec=Client)
    mock_client.send_message = AsyncMock(return_value=[MagicMock(), MagicMock()])

    msg = Message.model_validate(
        {
            "1": {"1": 1, "2": 555},
            "2": 999,
            "3": 1700000000,
            "4": 10,
            "5": {"text": {"1": "Parent msg"}},
        },
        context={"client": mock_client},
    )

    very_long_err = "Traceback (most recent call last):\n" + ("  File 'test.py', line 10, in foo\n" * 40)
    await msg.reply(very_long_err, auto_split=True, max_split_length=500)

    mock_client.send_message.assert_awaited_once_with(
        text=very_long_err,
        chat_id=555,
        chat_type=ChatType.PRIVATE,
        reply_to=msg,
        message_id=None,
        reply_markup=None,
        auto_split=True,
        max_split_length=500,
        as_file_if_too_long=False,
        file_name="message.txt",
    )
