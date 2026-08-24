import pytest
import tempfile
import pathlib
from aiobale.utils.paginator import KeyboardPaginator
from aiobale.utils.throttler import MessageThrottler
from aiobale.utils.progress import format_bytes, create_progress_bar
from aiobale.cli.main import cmd_startproject


def test_keyboard_paginator_pages_and_items():
    items = [f"Item {i}" for i in range(1, 11)]  # 10 items
    paginator = KeyboardPaginator(items=items, page_size=3, callback_prefix="test")

    assert paginator.total_pages == 4
    page1_items = paginator.get_page_items(1)
    assert page1_items == ["Item 1", "Item 2", "Item 3"]

    page4_items = paginator.get_page_items(4)
    assert page4_items == ["Item 10"]

    markup1 = paginator.get_page(1)
    # 3 item rows + 1 nav row
    assert len(markup1) == 4
    # Nav row buttons: prev (disabled/noop), indicator, next
    nav_row = markup1[-1]
    assert len(nav_row) == 3
    assert nav_row[1]["text"] == "📄 1 / 4"
    assert nav_row[2]["callback_data"] == "test:2"


@pytest.mark.asyncio
async def test_message_throttler_broadcast():
    throttler = MessageThrottler(rate_limit=0.01)
    sent_targets = []

    async def mock_send(chat_id: int):
        sent_targets.append(chat_id)
        return "sent"

    targets = [101, 102, 103, 104]
    progress_records = []
    
    def on_progress(curr, total):
        progress_records.append((curr, total))

    result = await throttler.broadcast(mock_send, targets, progress_callback=on_progress)

    assert result.total == 4
    assert result.success_count == 4
    assert result.failure_count == 0
    assert sent_targets == targets
    assert len(progress_records) == 4
    assert progress_records[-1] == (4, 4)


def test_progress_bar_format():
    assert format_bytes(500) == "500 B"
    assert format_bytes(1024 * 50) == "50.0 KB"
    assert format_bytes(1024 * 1024 * 2.5) == "2.5 MB"
    assert format_bytes(1024 * 1024 * 1024 * 1.5) == "1.50 GB"

    cb = create_progress_bar("Testing")
    cb(50, 100)
    cb(100, 100)


def test_cli_startproject():
    with tempfile.TemporaryDirectory() as tmpdir:
        target_path = pathlib.Path(tmpdir) / "demo_bot"
        cmd_startproject(str(target_path))

        assert (target_path / "bot.py").exists()
        assert (target_path / "config.py").exists()
        assert (target_path / "handlers" / "common.py").exists()
        assert (target_path / "keyboards" / "inline.py").exists()
        assert (target_path / "middlewares" / "logging.py").exists()
