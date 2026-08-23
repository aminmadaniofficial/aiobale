from aiobale.types import (
    Message,
    Chat,
    MessageContent,
    TextMessage,
    DocumentMessage,
    QuotedMessage,
    Peer,
    IntValue,
)
from aiobale.types.responses import ContactResponse
from aiobale.types import InfoPeer
from aiobale.enums import ChatType, PeerType, TypingMode, GiftOpening, GiftOpenning


def test_message_quoted_reply_chat_attachment():
    chat = Chat(type=ChatType.GROUP, id=555)
    peer = Peer(type=PeerType.GROUP, id=555)
    quoted = QuotedMessage(
        message_id=IntValue(value=10),
        sender_id=20,
        date=1700000000000,
        content=MessageContent(text=TextMessage(value="original message")),
        peer=peer,
    )

    msg = Message(
        chat=chat,
        sender_id=30,
        date=1700000005000,
        message_id=11,
        content=MessageContent(text=TextMessage(value="reply")),
        quoted_replied_to=quoted,
    )

    assert msg.quoted_replied_to.chat is not None
    assert msg.quoted_replied_to.chat.id == 555
    assert msg.replied_to is not None
    assert msg.replied_to.message_id == 10
    assert msg.replied_to.chat.id == 555


def test_contact_response_fields():
    info_user = InfoPeer(id=1, access_hash=2, name="test_user")
    info_group = InfoPeer(id=10, access_hash=20, name="test_group")

    resp = ContactResponse(user=info_user, group=info_group)
    assert resp.user.name == "test_user"
    assert resp.group.name == "test_group"


def test_message_content_empty():
    content_empty = MessageContent.model_validate({"5": True})
    assert content_empty.empty is True

    content_text = MessageContent(text=TextMessage(value="test"))
    assert content_text.empty is False
    assert content_text.text.value == "test"


def test_enum_aliases():
    # TypingMode aliases
    assert TypingMode.VOICERECORDING == TypingMode.VOICERECODRING == 2
    assert TypingMode.CHOOSINGGIF == TypingMode.CHOSINGGIF == 9
    assert TypingMode.CHOOSINGEMOJI == TypingMode.CHOSINGEMOJI == 12

    # GiftOpening alias
    assert GiftOpening is GiftOpenning
