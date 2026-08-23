from aiobale.types import (
    Update,
    UpdateBody,
    Message,
    Chat,
    MessageContent,
    TextMessage,
    UpdatedMessage,
    Peer,
    IntValue,
)
from aiobale.enums import ChatType, PeerType


def test_update_current_event_message():
    msg = Message(
        chat=Chat(type=ChatType.PRIVATE, id=10),
        sender_id=20,
        date=1700000000000,
        message_id=100,
        content=MessageContent(text=TextMessage(value="test update")),
    )
    upd = Update(message=msg)
    assert upd.current_event is not None
    event_type, event_val = upd.current_event
    assert event_type == "message"
    assert event_val is msg


def test_update_current_event_message_edited():
    updated_msg = UpdatedMessage(
        peer=Peer(type=PeerType.PRIVATE, id=10),
        message_id=100,
        content=MessageContent(text=TextMessage(value="edited text")),
        date=IntValue(value=1700000001000),
        sender_id=IntValue(value=20),
    )
    upd = Update(message_edited=updated_msg)
    assert upd.current_event is not None
    event_type, event_val = upd.current_event
    assert event_type == "message_edited"
    # Reconstructed Message should be accessible
    assert isinstance(event_val, Message)
    assert event_val.text == "edited text"
    assert event_val.message_id == 100
