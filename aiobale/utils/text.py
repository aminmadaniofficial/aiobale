from __future__ import annotations
from typing import List


def smart_split_text(text: str, max_length: int = 4000) -> List[str]:
    """
    Intelligently splits a long string into chunks of at most `max_length` characters,
    preferring split points at newlines (`\n`) or spaces without breaking words.

    Args:
        text (str): The string to split.
        max_length (int): Maximum character length of each chunk (defaults to 4000).

    Returns:
        List[str]: List of split string chunks.
    """
    if not text:
        return [""]

    if len(text) <= max_length:
        return [text]

    chunks: List[str] = []
    remaining = text

    while len(remaining) > max_length:
        # 1. Try splitting at the last newline within max_length
        split_idx = remaining.rfind("\n", 0, max_length)

        # 2. If no newline found, try splitting at the last space
        if split_idx == -1 or split_idx == 0:
            split_idx = remaining.rfind(" ", 0, max_length)

        # 3. If no whitespace found, hard cut at max_length
        if split_idx == -1 or split_idx == 0:
            split_idx = max_length

        chunk = remaining[:split_idx].rstrip()
        if chunk:
            chunks.append(chunk)

        remaining = remaining[split_idx:]
        if remaining.startswith("\n") or remaining.startswith("\r\n"):
            remaining = remaining.lstrip("\r\n")
        elif remaining.startswith(" "):
            remaining = remaining[1:]

    if remaining.strip():
        chunks.append(remaining)

    return chunks or [text]
