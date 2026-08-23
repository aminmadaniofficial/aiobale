import pytest
from aiobale import Dispatcher, Router, Client, F
from aiobale.enums import ChatType
from aiobale.filters import (
    IsText,
    IsDocument,
    IsGift,
    IsPrivate,
    IsGroupOrChannel,
    ChatTypeFilter,
    RegexFilter,
    and_f,
    or_f,
    invert_f,
)
from aiobale.types import (
    Message,
    Chat,
    MessageContent,
    TextMessage,
    DocumentMessage,
)


@pytest.mark.asyncio
async def test_dispatcher_message_handling():
    dp = Dispatcher()
    received = []

    @dp.message(IsText())
    async def on_text(msg: Message, client: Client):
        received.append((msg.text, client))

    client = Client(dp, session_file=None, token="dummy")
    msg = Message(
        chat=Chat(type=ChatType.PRIVATE, id=123),
        sender_id=456,
        date=1700000000000,
        message_id=1,
        content=MessageContent(text=TextMessage(value="Hello Bale!")),
    )

    await dp.dispatch("message", msg, client=client)
    assert len(received) == 1
    assert received[0][0] == "Hello Bale!"
    assert received[0][1] is client


@pytest.mark.asyncio
async def test_dispatcher_magic_filter():
    dp = Dispatcher()
    received = []

    @dp.message(F.text == "ping")
    async def on_ping(msg: Message):
        received.append("pong")

    msg_ping = Message(
        chat=Chat(type=ChatType.PRIVATE, id=123),
        sender_id=456,
        date=1700000000000,
        message_id=1,
        content=MessageContent(text=TextMessage(value="ping")),
    )
    msg_other = Message(
        chat=Chat(type=ChatType.PRIVATE, id=123),
        sender_id=456,
        date=1700000000000,
        message_id=2,
        content=MessageContent(text=TextMessage(value="pong")),
    )

    await dp.dispatch("message", msg_other)
    assert len(received) == 0

    await dp.dispatch("message", msg_ping)
    assert received == ["pong"]


@pytest.mark.asyncio
async def test_dispatcher_logic_filters():
    dp = Dispatcher()
    results = []

    @dp.message(and_f(IsText(), IsPrivate()))
    async def on_private_text(msg: Message):
        results.append("private_text")

    @dp.message(invert_f(IsText()))
    async def on_non_text(msg: Message):
        results.append("non_text")

    msg_text = Message(
        chat=Chat(type=ChatType.PRIVATE, id=123),
        sender_id=456,
        date=1700000000000,
        message_id=1,
        content=MessageContent(text=TextMessage(value="hi")),
    )
    msg_doc = Message(
        chat=Chat(type=ChatType.PRIVATE, id=123),
        sender_id=456,
        date=1700000000000,
        message_id=2,
        content=MessageContent(
            document=DocumentMessage(
                file_id=1, access_hash=2, mime_type="image/jpeg", name="pic.jpg"
            )
        ),
    )

    await dp.dispatch("message", msg_text)
    assert results == ["private_text"]

    await dp.dispatch("message", msg_doc)
    assert results == ["private_text", "non_text"]


@pytest.mark.asyncio
async def test_dispatcher_non_message_events():
    dp = Dispatcher()
    events_received = {}

    @dp.message_edited()
    async def on_edited(event):
        events_received["edited"] = event

    @dp.user_blocked()
    async def on_blocked(event):
        events_received["blocked"] = event

    await dp.dispatch("message_edited", "edited_event_obj")
    await dp.dispatch("user_blocked", "blocked_event_obj")

    assert events_received["edited"] == "edited_event_obj"
    assert events_received["blocked"] == "blocked_event_obj"
