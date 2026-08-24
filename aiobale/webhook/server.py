from __future__ import annotations
import asyncio
import json
from typing import TYPE_CHECKING, Any, Dict, Optional
from aiohttp import web

if TYPE_CHECKING:
    from ..client.client import Client


class AiohttpWebhookServer:
    """
    Lightweight asynchronous Webhook HTTP server for handling incoming bot updates.

    Example:
        ```python
        webhook = AiohttpWebhookServer(
            client=client,
            path="/webhook",
            secret_token="my_secret_key"
        )
        webhook.run(host="0.0.0.0", port=8080)
        ```
    """

    def __init__(
        self,
        client: Client,
        path: str = "/webhook",
        secret_token: Optional[str] = None,
    ) -> None:
        self.client = client
        self.path = path
        self.secret_token = secret_token
        self.app = web.Application()
        self._setup_routes()

    def _setup_routes(self) -> None:
        self.app.router.add_post(self.path, self._handle_webhook)
        self.app.router.add_get(self.path, self._handle_health)
        self.app.router.add_get("/health", self._handle_health)

    async def _handle_health(self, request: web.Request) -> web.Response:
        return web.json_response(
            {"status": "active", "server": "aiobale-webhook", "path": self.path}
        )

    async def _handle_webhook(self, request: web.Request) -> web.Response:
        if self.secret_token:
            token = request.headers.get("X-Bale-Bot-Api-Secret-Token")
            if token != self.secret_token:
                return web.Response(status=403, text="Forbidden: Invalid secret token")

        try:
            payload = await request.json()
        except Exception:
            return web.Response(status=400, text="Bad Request: Expected JSON")

        asyncio.create_task(self._process_payload(payload))
        return web.json_response({"ok": True})

    async def _process_payload(self, payload: Dict[str, Any]) -> None:
        if self.client.dispatcher:
            try:
                await self.client.dispatcher.dispatch(
                    "update", payload, client=self.client
                )
            except Exception as e:
                print(f"[Webhook Error] Error processing update payload: {e}")

    def run(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """Starts the aiohttp HTTP server synchronously."""
        web.run_app(self.app, host=host, port=port)
