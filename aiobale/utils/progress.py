from __future__ import annotations
import sys
import time
from typing import Callable, Optional


def format_bytes(size_bytes: float) -> str:
    """Formats bytes to human-readable string (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes:.0f} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.2f} GB"


def create_progress_bar(
    description: str = "Transferring",
    bar_length: int = 25,
    fill_char: str = "█",
    empty_char: str = "░",
) -> Callable[[int, Optional[int]], None]:
    """
    Creates an interactive CLI progress bar callback suitable for `upload_file` and `download_file`.

    Example:
        ```python
        cb = create_progress_bar("Uploading Video")
        await client.upload_file("video.mp4", progress_callback=cb)
        ```
    """
    start_time = time.time()
    last_update = 0.0

    def progress_callback(current: int, total: Optional[int] = None) -> None:
        nonlocal last_update
        now = time.time()
        # Throttle terminal redraws to max 10 updates per second
        if total and current < total and (now - last_update) < 0.1:
            return
        last_update = now

        elapsed = max(0.001, now - start_time)
        speed = current / elapsed
        speed_str = f"{format_bytes(speed)}/s"

        if total and total > 0:
            percent = min(100.0, (current / total) * 100.0)
            filled_len = int(bar_length * current // total)
            bar = fill_char * filled_len + empty_char * (bar_length - filled_len)
            size_str = f"{format_bytes(current)} / {format_bytes(total)}"
            output = f"\r{description}: [{bar}] {percent:.1f}% ({size_str}) at {speed_str}"
        else:
            size_str = format_bytes(current)
            output = f"\r{description}: {size_str} transferred at {speed_str}"

        sys.stdout.write(output)
        sys.stdout.flush()

        if total and current >= total:
            sys.stdout.write("\n")
            sys.stdout.flush()

    return progress_callback
