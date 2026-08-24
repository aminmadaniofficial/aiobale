import pytest
from aiobale import Dispatcher, F
from aiobale.fsm import State, StatesGroup, FSMContext
from aiobale.types import Message, Chat, MessageContent, TextMessage
from aiobale.enums import ChatType


class OrderForm(StatesGroup):
    choosing_item = State()
    choosing_quantity = State()


@pytest.mark.asyncio
async def test_dispatcher_fsm_flow():
    dp = Dispatcher()

    @dp.message(F.text == "/order")
    async def start_order(msg: Message, state: FSMContext):
        await state.set_state(OrderForm.choosing_item)
        return "state_set_to_item"

    @dp.message(OrderForm.choosing_item)
    async def item_chosen(msg: Message, state: FSMContext):
        await state.update_data(item=msg.text)
        await state.set_state(OrderForm.choosing_quantity)
        return f"saved_item_{msg.text}"

    @dp.message(OrderForm.choosing_quantity)
    async def quantity_chosen(msg: Message, state: FSMContext):
        data = await state.get_data()
        item = data.get("item")
        await state.clear()
        return f"order_completed_{item}_{msg.text}"

    chat = Chat(id=10, type=ChatType.PRIVATE)

    # Step 1: send /order
    msg1 = Message(
        chat=chat,
        sender_id=99,
        date=1700000000000,
        message_id=1,
        content=MessageContent(text=TextMessage(value="/order")),
    )
    res1 = await dp.dispatch("message", msg1)
    assert res1 == "state_set_to_item"

    # Step 2: send item name "Pizza"
    msg2 = Message(
        chat=chat,
        sender_id=99,
        date=1700000000000,
        message_id=2,
        content=MessageContent(text=TextMessage(value="Pizza")),
    )
    res2 = await dp.dispatch("message", msg2)
    assert res2 == "saved_item_Pizza"

    # Step 3: send quantity "2"
    msg3 = Message(
        chat=chat,
        sender_id=99,
        date=1700000000000,
        message_id=3,
        content=MessageContent(text=TextMessage(value="2")),
    )
    res3 = await dp.dispatch("message", msg3)
    assert res3 == "order_completed_Pizza_2"
