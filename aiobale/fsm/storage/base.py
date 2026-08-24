from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseStorage(ABC):
    """
    Abstract base storage for FSM states and data.
    """
    @abstractmethod
    async def set_state(self, chat_id: int, user_id: int, state: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def get_state(self, chat_id: int, user_id: int) -> Optional[str]:
        pass

    @abstractmethod
    async def set_data(self, chat_id: int, user_id: int, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def get_data(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update_data(self, chat_id: int, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def clear(self, chat_id: int, user_id: int) -> None:
        pass
