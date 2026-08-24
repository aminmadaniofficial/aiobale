from __future__ import annotations
import asyncio
import pathlib
from typing import List, Optional, Sequence, Union

from .client import Client
from ..dispatcher.dispatcher import Dispatcher


class ClientManager:
    """
    Manager for orchestrating multiple Aiobale clients simultaneously within a single event loop.

    Example:
        ```python
        dp = Dispatcher()
        manager = ClientManager(dp)
        manager.add_client(session_file="bot1.bale", phone_number="09121111111")
        manager.add_client(session_file="bot2.bale", token="JWT_TOKEN_...")

        manager.run_all()
        ```
    """

    def __init__(self, dispatcher: Optional[Dispatcher] = None) -> None:
        self.dispatcher: Optional[Dispatcher] = dispatcher
        self._clients: List[Client] = []

    @property
    def clients(self) -> List[Client]:
        """Returns the list of registered clients."""
        return list(self._clients)

    def add_client(
        self,
        client_or_session: Optional[Union[Client, str, pathlib.Path]] = None,
        **kwargs,
    ) -> Client:
        """
        Adds a new client to the manager.
        """
        if isinstance(client_or_session, Client):
            client = client_or_session
        else:
            if "dispatcher" not in kwargs:
                kwargs["dispatcher"] = self.dispatcher
            if "session_file" not in kwargs and client_or_session is not None:
                kwargs["session_file"] = client_or_session
            client = Client(**kwargs)

        self._clients.append(client)
        return client

    async def start_all(self) -> None:
        """Starts all registered clients concurrently."""
        if not self._clients:
            return
        await asyncio.gather(*(client.start() for client in self._clients))

    async def stop_all(self) -> None:
        """Stops all running clients cleanly."""
        for client in self._clients:
            await client.stop()

    def run_all(self) -> None:
        """Convenience method to start all clients in a blocking event loop."""
        try:
            asyncio.run(self.start_all())
        except (KeyboardInterrupt, SystemExit):
            pass
