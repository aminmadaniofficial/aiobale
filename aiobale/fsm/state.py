from __future__ import annotations
from typing import Optional, Set


class State:
    """
    Represents a specific conversational state in the Finite State Machine (FSM).
    """
    def __init__(self, state: Optional[str] = None, group_name: Optional[str] = None):
        self._state = state
        self._group_name = group_name

    @property
    def state(self) -> Optional[str]:
        if self._state is not None and self._group_name is not None:
            return f"{self._group_name}:{self._state}"
        return self._state

    def __str__(self) -> str:
        return self.state or ""

    def __repr__(self) -> str:
        return f"<State '{self.state}'>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.state == other.state
        if isinstance(other, str):
            return self.state == other
        return False

    def __hash__(self) -> int:
        return hash(self.state)


class StatesGroupMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        states: Set[State] = set()
        for key, value in namespace.items():
            if isinstance(value, State):
                value._state = key
                value._group_name = name
                states.add(value)
        cls._states = states
        cls._group_name = name
        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    """
    Base class for declaring groups of states.
    
    Example:
        class Registration(StatesGroup):
            name = State()
            phone = State()
            age = State()
    """
    _states: Set[State] = set()
    _group_name: str = ""

    @classmethod
    def get_states(cls) -> Set[State]:
        return cls._states


default_state = State(state="*default*")
any_state = State(state="*any*")
