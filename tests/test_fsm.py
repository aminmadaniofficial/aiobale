import pytest
from aiobale.fsm import State, StatesGroup, FSMContext, MemoryStorage, StateFilter, default_state, any_state


class TestForm(StatesGroup):
    step_one = State()
    step_two = State()


@pytest.mark.asyncio
async def test_fsm_state_declaration():
    assert TestForm.step_one.state == "TestForm:step_one"
    assert TestForm.step_two.state == "TestForm:step_two"
    assert str(TestForm.step_one) == "TestForm:step_one"
    assert TestForm.step_one == "TestForm:step_one"
    assert len(TestForm.get_states()) == 2


@pytest.mark.asyncio
async def test_fsm_storage_and_context():
    storage = MemoryStorage()
    ctx = FSMContext(storage=storage, chat_id=100, user_id=200)

    # Initial state should be None
    assert await ctx.get_state() is None
    assert await ctx.get_data() == {}

    # Set state
    await ctx.set_state(TestForm.step_one)
    assert await ctx.get_state() == "TestForm:step_one"

    # Update data
    await ctx.update_data(name="Ali", age=25)
    data = await ctx.get_data()
    assert data == {"name": "Ali", "age": 25}

    # Transition state
    await ctx.set_state(TestForm.step_two)
    assert await ctx.get_state() == "TestForm:step_two"

    # Clear
    await ctx.clear()
    assert await ctx.get_state() is None
    assert await ctx.get_data() == {}


@pytest.mark.asyncio
async def test_state_filter():
    storage = MemoryStorage()
    ctx = FSMContext(storage=storage, chat_id=1, user_id=2)

    filter_default = StateFilter(default_state)
    filter_step1 = StateFilter(TestForm.step_one)
    filter_any = StateFilter(any_state)

    # Default state (None)
    assert await filter_default(None, state=ctx) is True
    assert await filter_step1(None, state=ctx) is False
    assert await filter_any(None, state=ctx) is True

    # After setting step_one
    await ctx.set_state(TestForm.step_one)
    assert await filter_default(None, state=ctx) is False
    assert await filter_step1(None, state=ctx) is True
    assert await filter_any(None, state=ctx) is True
