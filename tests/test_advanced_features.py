import pytest
import tempfile
import pathlib
from aiobale import Dispatcher, F, Command, CommandObject, CallbackData, SQLiteStorage, ClientManager, Client
from aiobale.client.auth_cli import PhoneLoginCLI
from aiobale.types import Message, Chat, MessageContent, TextMessage
from aiobale.enums import ChatType


class OrderCB(CallbackData, prefix="order"):
    item_id: int
    confirmed: bool


def test_callback_data_packing_and_unpacking():
    cb = OrderCB(item_id=42, confirmed=True)
    packed = cb.pack()
    assert packed == "order:42:True"

    unpacked = OrderCB.unpack(packed)
    assert unpacked.item_id == 42
    assert unpacked.confirmed is True


@pytest.mark.asyncio
async def test_command_filter_parsing_and_injection():
    dp = Dispatcher()
    received_commands = []

    @dp.message(Command("ban", "kick", prefix="/!"))
    async def handle_ban(msg: Message, command: CommandObject):
        received_commands.append((command.command, command.args, command.args_list))
        return "ban_ok"

    chat = Chat(id=1, type=ChatType.GROUP)
    msg1 = Message(
        chat=chat,
        sender_id=123,
        date=1700000000000,
        message_id=1,
        content=MessageContent(text=TextMessage(value="!ban 98765 10m spam")),
    )
    res1 = await dp.dispatch("message", msg1)
    assert res1 == "ban_ok"
    assert len(received_commands) == 1
    assert received_commands[0][0] == "ban"
    assert received_commands[0][1] == "98765 10m spam"
    assert received_commands[0][2] == ["98765", "10m", "spam"]


@pytest.mark.asyncio
async def test_sqlite_storage():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = pathlib.Path(tmpdir) / "test_fsm.db"
        storage = SQLiteStorage(db_file)

        # Set state and data
        await storage.set_state(chat_id=10, user_id=20, state="MyState:step1")
        await storage.set_data(chat_id=10, user_id=20, data={"step": 1, "name": "Amin"})

        assert await storage.get_state(chat_id=10, user_id=20) == "MyState:step1"
        assert await storage.get_data(chat_id=10, user_id=20) == {"step": 1, "name": "Amin"}

        # Update data
        await storage.update_data(chat_id=10, user_id=20, data={"score": 100})
        data = await storage.get_data(chat_id=10, user_id=20)
        assert data == {"step": 1, "name": "Amin", "score": 100}

        # Clear
        await storage.clear(chat_id=10, user_id=20)
        assert await storage.get_state(chat_id=10, user_id=20) is None
        assert await storage.get_data(chat_id=10, user_id=20) == {}


def test_phone_normalization():
    assert PhoneLoginCLI.normalize_phone_number("09123456789") == 989123456789
    assert PhoneLoginCLI.normalize_phone_number("+989123456789") == 989123456789
    assert PhoneLoginCLI.normalize_phone_number("00989123456789") == 989123456789
    assert PhoneLoginCLI.normalize_phone_number(989123456789) == 989123456789


def test_client_manager():
    dp = Dispatcher()
    manager = ClientManager(dp)
    c1 = manager.add_client(session_file=None, token="tok1")
    c2 = manager.add_client(session_file=None, token="tok2")

    assert len(manager.clients) == 2
    assert manager.clients[0] is c1
    assert manager.clients[1] is c2
