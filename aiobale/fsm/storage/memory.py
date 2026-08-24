from __future__ import annotations
from typing import Any, Dict, Optional, Tuple
from .base import BaseStorage


class MemoryStorage(BaseStorage):
    """
    In-memory storage for FSM states and contextual data.
    """
    def __init__(self) -> None:
        self._states: Dict[Tuple[int, int], Optional[str]] = {}
        self._data: Dict[Tuple[int, int], Dict[str, Any]] = {}

    def _key(self, chat_id: int, user_id: int) -> Tuple[int, int]:
        return (chat_id, user_id)

    async def set_state(self, chat_id: int, user_id: int, state: Optional[str] = None) -> None:
        key = self._key(chat_id, user_id)
        if state is None:
            self._states.pop(key, None)
        else:
            self._states[key] = state

    async def get_state(self, chat_id: int, user_id: int) -> Optional[str]:
        return self._states.get(self._key(chat_id, user_id))

    async def set_data(self, chat_id: int, user_id: int, data: Dict[str, Any]) -> None:
        self._data[self._key(chat_id, user_id)] = data.copy()

    async def get_data(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        return self._data.get(self._key(chat_id, user_id), {}).copy()

    async def update_data(self, chat_id: int, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        key = self._key(chat_id, user_id)
        current = self._data.setdefault(key, {})
        current.update(data)
        return current.copy()

    async def clear(self, chat_id: int, user_id: int) -> None:
        key = self._key(chat_id, user_id)
        self._states.pop(key, None)
        self._data.pop(key, None)
