import pytest
from unittest.mock import MagicMock
from aiobale import Client
from aiobale.types import UserAuth, Chat, ShortPeer
from aiobale.methods.groups import InviteUsers
from aiobale.enums import ChatType


@pytest.mark.asyncio
async def test_invite_users_flexible_args():
    client = Client(token="dummy_token")
    
    captured_call = None
    async def fake_handler(method, **kwargs):
        nonlocal captured_call
        captured_call = method
        return MagicMock()

    client.session.post = fake_handler
    client.session.make_request = fake_handler

    # 1. Standard (chat_id, single int user)
    await client.invite_users(chat_id=1001, users=2002)
    assert isinstance(captured_call, InviteUsers)
    assert captured_call.group.id == 1001
    assert len(captured_call.users) == 1
    assert captured_call.users[0].id == 2002

    # 2. Standard (chat_id, list of int users)
    await client.invite_users(chat_id=1001, users=[2002, 3003])
    assert captured_call.group.id == 1001
    assert len(captured_call.users) == 2
    assert captured_call.users[0].id == 2002
    assert captured_call.users[1].id == 3003

    # 3. With UserAuth and Chat objects
    user_obj = UserAuth(id=4004, access_hash=1, name="TestUser")
    chat_obj = Chat(id=5005, type=ChatType.GROUP)
    await client.invite_users(chat_id=chat_obj, users=user_obj)
    assert captured_call.group.id == 5005
    assert len(captured_call.users) == 1
    assert captured_call.users[0].id == 4004

    # 4. Inverted legacy ordering (users_list, chat_id)
    await client.invite_users([6006, 7007], 8008)
    assert captured_call.group.id == 8008
    assert len(captured_call.users) == 2
    assert captured_call.users[0].id == 6006
    assert captured_call.users[1].id == 7007

    # 5. Single user alias: invite_user
    await client.invite_user(chat_id=9009, user=1111)
    assert captured_call.group.id == 9009
    assert len(captured_call.users) == 1
    assert captured_call.users[0].id == 1111
