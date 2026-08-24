from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence, Union


@dataclass
class BroadcastResult:
    """Result summary of a broadcast operation."""
    total: int
    success_count: int = 0
    failure_count: int = 0
    errors: Dict[int, str] = field(default_factory=dict)
    duration_seconds: float = 0.0


class MessageThrottler:
    """
    Asynchronous message queue and rate-limiter to prevent flood-wait errors when sending high volume messages.

    Parameters:
        rate_limit (float): Delay in seconds between requests (e.g. 0.05 for 20 requests/sec).
        max_retries (int): Number of automatic retries on network/flood errors.
    """

    def __init__(self, rate_limit: float = 0.05, max_retries: int = 3) -> None:
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self._lock = asyncio.Lock()
        self._last_call_time = 0.0

    async def execute(
        self,
        func: Callable[..., Awaitable[Any]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Executes a single async callable while respecting the rate limit."""
        async with self._lock:
            now = time.time()
            elapsed = now - self._last_call_time
            if elapsed < self.rate_limit:
                await asyncio.sleep(self.rate_limit - elapsed)
            self._last_call_time = time.time()

        for attempt in range(1, self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise e
                await asyncio.sleep(attempt * 0.5)

    async def broadcast(
        self,
        send_fn: Callable[[int], Awaitable[Any]],
        chat_ids: Sequence[int],
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> BroadcastResult:
        """
        Safely sends a message/action to multiple chat IDs with rate-limiting and progress tracking.

        Args:
            send_fn: Async callable taking `chat_id` as its first argument.
            chat_ids: Sequence of target user/chat IDs.
            progress_callback: Optional callback receiving `(current_index, total_count)`.
        """
        start_time = time.time()
        result = BroadcastResult(total=len(chat_ids))

        for idx, chat_id in enumerate(chat_ids, 1):
            try:
                await self.execute(send_fn, chat_id)
                result.success_count += 1
            except Exception as e:
                result.failure_count += 1
                result.errors[chat_id] = str(e)

            if progress_callback:
                progress_callback(idx, result.total)

        result.duration_seconds = time.time() - start_time
        return result
