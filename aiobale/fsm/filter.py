from __future__ import annotations
from typing import Any, Optional, Sequence, Union
from ..filters.base import Filter
from .state import State, any_state, default_state
from .context import FSMContext


class StateFilter(Filter):
    """
    Filter to match against FSM states.
    
    Example:
        @dp.message(StateFilter(MyState.step1))
        async def step1_handler(msg: Message, state: FSMContext):
            ...
    """
    def __init__(self, *states: Optional[Union[State, str, Sequence[Union[State, str]], type]]):
        from .state import StatesGroup
        flat_states = []
        for s in states:
            if isinstance(s, type) and issubclass(s, StatesGroup):
                flat_states.extend(s.get_states())
            elif isinstance(s, (list, tuple, set)):
                flat_states.extend(s)
            else:
                flat_states.append(s)
        self.states = [s.state if isinstance(s, State) else s for s in flat_states]

    async def __call__(self, event: Any, state: Optional[FSMContext] = None) -> bool:
        if state is None:
            return False
        current_state = await state.get_state()
        if any_state.state in self.states or any_state in self.states:
            return True
        if None in self.states or default_state.state in self.states:
            if current_state is None:
                return True
        return current_state in self.states
