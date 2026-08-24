import pytest
from typing import Any, Awaitable, Callable, Dict
from aiobale import Dispatcher, BaseMiddleware
from aiobale.types import Message, Chat, MessageContent, TextMessage
from aiobale.enums import ChatType


class CounterMiddleware(BaseMiddleware):
    def __init__(self):
        self.pre_count = 0
        self.post_count = 0

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        self.pre_count += 1
        data["injected_value"] = "secret_123"
        result = await handler(event, data)
        self.post_count += 1
        return result


@pytest.mark.asyncio
async def test_middleware_execution_flow():
    dp = Dispatcher()
    mw = CounterMiddleware()
    dp.middleware(mw)

    called = False
    injected_result = None

    @dp.message()
    async def handler(msg: Message, injected_value: str = None):
        nonlocal called, injected_result
        called = True
        injected_result = injected_value
        return "handler_ok"

    dummy_msg = Message(
        chat=Chat(id=123, type=ChatType.PRIVATE),
        sender_id=456,
        date=1700000000000,
        message_id=1,
        content=MessageContent(text=TextMessage(value="hello")),
    )

    res = await dp.dispatch("message", dummy_msg)

    assert called is True
    assert res == "handler_ok"
    assert mw.pre_count == 1
    assert mw.post_count == 1
    assert injected_result == "secret_123"
