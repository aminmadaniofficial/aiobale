from __future__ import annotations
import asyncio
import json
import sqlite3
import pathlib
from typing import Any, Dict, Optional, Union

from .base import BaseStorage
from ..state import State
from ...utils.compat import to_thread


class SQLiteStorage(BaseStorage):
    """
    Persistent SQLite storage backend for FSM (Finite State Machine).
    Stores conversation states and associated data in a local SQLite database file.

    Parameters:
        db_path (Union[str, pathlib.Path]): Path to the SQLite database file. Defaults to 'fsm_storage.db'.
    """

    def __init__(self, db_path: Union[str, pathlib.Path] = "fsm_storage.db") -> None:
        self.db_path = str(db_path)
        self._init_db_sync()

    def _init_db_sync(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS fsm_storage (
                    chat_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    state TEXT,
                    data TEXT,
                    PRIMARY KEY (chat_id, user_id)
                )
                """
            )
            conn.commit()

    async def set_state(
        self,
        chat_id: int,
        user_id: int,
        state: Optional[Union[str, State]] = None,
    ) -> None:
        state_str = state.state if isinstance(state, State) else state

        def _sync_set_state():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO fsm_storage (chat_id, user_id, state, data)
                    VALUES (?, ?, ?, '{}')
                    ON CONFLICT(chat_id, user_id) DO UPDATE SET state = excluded.state
                    """,
                    (chat_id, user_id, state_str),
                )
                conn.commit()

        await to_thread(_sync_set_state)

    async def get_state(self, chat_id: int, user_id: int) -> Optional[str]:
        def _sync_get_state():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT state FROM fsm_storage WHERE chat_id = ? AND user_id = ?",
                    (chat_id, user_id),
                )
                row = cursor.fetchone()
                return row[0] if row else None

        return await to_thread(_sync_get_state)

    async def set_data(
        self,
        chat_id: int,
        user_id: int,
        data: Dict[str, Any],
    ) -> None:
        data_json = json.dumps(data)

        def _sync_set_data():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO fsm_storage (chat_id, user_id, state, data)
                    VALUES (?, ?, NULL, ?)
                    ON CONFLICT(chat_id, user_id) DO UPDATE SET data = excluded.data
                    """,
                    (chat_id, user_id, data_json),
                )
                conn.commit()

        await to_thread(_sync_set_data)

    async def get_data(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        def _sync_get_data():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data FROM fsm_storage WHERE chat_id = ? AND user_id = ?",
                    (chat_id, user_id),
                )
                row = cursor.fetchone()
                if row and row[0]:
                    try:
                        return json.loads(row[0])
                    except Exception:
                        return {}
                return {}

        return await to_thread(_sync_get_data)

    async def update_data(
        self,
        chat_id: int,
        user_id: int,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        current_data = await self.get_data(chat_id=chat_id, user_id=user_id)
        current_data.update(data)
        await self.set_data(chat_id=chat_id, user_id=user_id, data=current_data)
        return current_data

    async def clear(self, chat_id: int, user_id: int) -> None:
        def _sync_clear():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM fsm_storage WHERE chat_id = ? AND user_id = ?",
                    (chat_id, user_id),
                )
                conn.commit()

        await to_thread(_sync_clear)

    async def close(self) -> None:
        pass
