from __future__ import annotations
from typing import Any, Dict, Optional, Union
from .state import State
from .storage.base import BaseStorage


class FSMContext:
    """
    Contextual wrapper providing easy access to state and data for a given (chat_id, user_id).
    """
    def __init__(self, storage: BaseStorage, chat_id: int, user_id: int):
        self.storage = storage
        self.chat_id = chat_id
        self.user_id = user_id

    async def set_state(self, state: Optional[Union[State, str]] = None) -> None:
        state_str = state.state if isinstance(state, State) else state
        await self.storage.set_state(self.chat_id, self.user_id, state_str)

    async def get_state(self) -> Optional[str]:
        return await self.storage.get_state(self.chat_id, self.user_id)

    async def set_data(self, data: Dict[str, Any]) -> None:
        await self.storage.set_data(self.chat_id, self.user_id, data)

    async def get_data(self) -> Dict[str, Any]:
        return await self.storage.get_data(self.chat_id, self.user_id)

    async def update_data(self, **kwargs: Any) -> Dict[str, Any]:
        return await self.storage.update_data(self.chat_id, self.user_id, kwargs)

    async def clear(self) -> None:
        await self.storage.clear(self.chat_id, self.user_id)
