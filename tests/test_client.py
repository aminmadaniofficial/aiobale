import pytest
from unittest.mock import AsyncMock, patch
from aiobale import Client, Dispatcher
from aiobale.enums import AuthErrors, ChatType
from aiobale.exceptions import AiobaleError
from aiobale.types import Message, Chat, MessageContent, TextMessage


def test_client_init_none_session_file():
    # Should not raise TypeError when session_file is None
    client = Client(session_file=None)
    assert client.session_file is None
    assert client.id is None
    assert client.me is None


def test_client_init_token():
    # Can initialize with direct token string
    client = Client(session_file=None, token="test_token_123")
    assert client.token == "test_token_123"
    assert client.session_file is None


def test_client_id_unauthenticated():
    client = Client(session_file=None)
    # Should safely return None without throwing AttributeError
    assert client.id is None


def test_client_should_ignore():
    client = Client(session_file=None)

    # 1. Normal message not sent by this client should NOT be ignored
    msg = Message(
        chat=Chat(type=ChatType.PRIVATE, id=100),
        sender_id=200,
        date=1700000000000,
        message_id=999,
        content=MessageContent(text=TextMessage(value="hello")),
    )
    assert client._should_ignore("message", msg) is False

    # 2. Self-sent message in targets SHOULD be ignored once
    client._ignored_messages.targets.append(999)
    assert client._should_ignore("message", msg) is True
    # And removed after ignoring:
    assert client._should_ignore("message", msg) is False

    # 3. Non-message events MUST NEVER be ignored
    for event_type in [
        "message_edited",
        "message_deleted",
        "chat_deleted",
        "chat_cleared",
        "user_blocked",
        "user_unblocked",
        "group_message_pinned",
        "group_pin_removed",
        "username_changed",
        "about_changed",
    ]:
        dummy_event = object()
        assert (
            client._should_ignore(event_type, dummy_event) is False
        ), f"Event {event_type} was incorrectly ignored!"


@pytest.mark.asyncio
async def test_start_phone_auth_blocked_number():
    client = Client(session_file=None)
    client.session.post = AsyncMock(return_value="phone number is blocked")

    result = await client.start_phone_auth(989123456789)
    assert result == AuthErrors.NUMBER_BANNED

    client.session.post = AsyncMock(return_value="PHONE_NUMBER_TEMPORARY_BLOCKED")
    result = await client.start_phone_auth(989123456789)
    assert result == AuthErrors.NUMBER_BANNED

    client.session.post = AsyncMock(return_value="phone auth limit exceeded")
    result = await client.start_phone_auth(989123456789)
    assert result == AuthErrors.RATE_LIMIT

    client.session.post = AsyncMock(return_value="PHONE_NUMBER_INVALID")
    result = await client.start_phone_auth(989123456789)
    assert result == AuthErrors.INVALID


@pytest.mark.asyncio
async def test_ensure_token_exists_headless_error():
    client = Client(session_file=None)
    with patch("sys.stdin.isatty", return_value=False):
        with pytest.raises(AiobaleError) as excinfo:
            await client._ensure_token_exists()
        assert "interactive login is not supported" in str(excinfo.value)
