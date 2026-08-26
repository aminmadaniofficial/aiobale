import io
import pathlib
import pytest
from typing import Optional
from unittest.mock import AsyncMock, MagicMock

from aiobale.types import FileInput, Message, Chat, MessageContent, DocumentMessage
from aiobale.fsm.context import FSMContext
from aiobale.fsm.storage.memory import MemoryStorage
from aiobale.fsm.state import StatesGroup, State
from aiobale.fsm.filter import StateFilter
from aiobale.utils.callback_data import CallbackData
from aiobale import Client
from aiobale.enums import ChatType


class SampleForm(StatesGroup):
    step_one = State()
    step_two = State()


class UserActionCB(CallbackData, prefix="act"):
    action: str
    user_id: Optional[int] = None
    count: int = 1


@pytest.mark.asyncio
async def test_file_input_bytes_io():
    buf = io.BytesIO(b"Hello Bale Stream!")
    buf.name = "test.txt"
    file_input = FileInput(buf)

    assert file_input.info.name == "test.txt"
    assert file_input.info.size == len(b"Hello Bale Stream!")

    content = await file_input.get_content()
    assert content == b"Hello Bale Stream!"


@pytest.mark.asyncio
async def test_file_input_ensure_helper(tmp_path: pathlib.Path):
    p = tmp_path / "sample.jpg"
    p.write_bytes(b"\xff\xd8\xff\xe0test_jpeg")

    # From Path / str
    f_path = FileInput.ensure(str(p))
    assert isinstance(f_path, FileInput)
    assert f_path.info.name == "sample.jpg"
    assert "image/jpeg" in f_path.info.mime_type

    # From bytes
    f_bytes = FileInput.ensure(b"%PDF-1.4 file content")
    assert isinstance(f_bytes, FileInput)
    assert f_bytes.info.mime_type == "application/pdf"

    # Already FileInput
    f_same = FileInput.ensure(f_bytes)
    assert f_same is f_bytes


@pytest.mark.asyncio
async def test_fsm_context_update_data_dict_and_kwargs():
    storage = MemoryStorage()
    ctx = FSMContext(storage, chat_id=123, user_id=456)

    # 1. Update via dict
    res1 = await ctx.update_data({"name": "Amin", "role": "admin"})
    assert res1 == {"name": "Amin", "role": "admin"}

    # 2. Update via kwargs
    res2 = await ctx.update_data(age=25, status="active")
    assert res2 == {"name": "Amin", "role": "admin", "age": 25, "status": "active"}

    # 3. Update with both
    res3 = await ctx.update_data({"city": "Tehran"}, score=100)
    assert res3["city"] == "Tehran"
    assert res3["score"] == 100
    assert (await ctx.get_data()) == res3


@pytest.mark.asyncio
async def test_callback_data_optional_types():
    cb = UserActionCB(action="view", user_id=998877, count=5)
    packed = cb.pack()
    assert packed == "act:view:998877:5"

    unpacked = UserActionCB.unpack(packed)
    assert unpacked.action == "view"
    assert unpacked.user_id == 998877
    assert isinstance(unpacked.user_id, int)
    assert unpacked.count == 5

    # Optional None handling
    cb_none = UserActionCB(action="list", user_id=None, count=1)
    packed_none = cb_none.pack()
    unpacked_none = UserActionCB.unpack(packed_none)
    assert unpacked_none.user_id is None
    assert unpacked_none.action == "list"


@pytest.mark.asyncio
async def test_state_filter_with_states_group():
    filter_group = StateFilter(SampleForm)
    storage = MemoryStorage()
    ctx = FSMContext(storage, chat_id=1, user_id=1)

    # Event dummy
    msg = MagicMock()

    # Initial state (None) -> should not match
    assert await filter_group(msg, state=ctx) is False

    # State set to step_one -> should match
    await ctx.set_state(SampleForm.step_one)
    assert await filter_group(msg, state=ctx) is True

    # State set to step_two -> should match
    await ctx.set_state(SampleForm.step_two)
    assert await filter_group(msg, state=ctx) is True

    # State set to other -> should not match
    await ctx.set_state("OtherGroup:custom_state")
    assert await filter_group(msg, state=ctx) is False


@pytest.mark.asyncio
async def test_message_download_helper():
    mock_client = MagicMock(spec=Client)
    mock_client.download_file = AsyncMock(return_value=io.BytesIO(b"downloaded file data"))

    msg = Message.model_validate(
        {
            "1": {"1": 1, "2": 123456},
            "2": 999,
            "3": 1700000000,
            "4": 555,
            "5": {
                "document": {
                    "file_id": 112233,
                    "access_hash": 445566,
                    "size": 20,
                    "name": "photo.jpg",
                    "mime_type": "image/jpeg",
                }
            },
        },
        context={"client": mock_client},
    )

    result = await msg.download()
    assert result.getvalue() == b"downloaded file data"
    mock_client.download_file.assert_awaited_once_with(
        file_id=112233,
        access_hash=445566,
        destination=None,
        seek=True,
    )
