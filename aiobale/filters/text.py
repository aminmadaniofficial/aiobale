from __future__ import annotations
from typing import Any, Sequence, Union
from .base import Filter
from ..types import Message


class TextEquals(Filter):
    """
    Filters messages whose text exactly matches one of the specified texts.
    """
    def __init__(self, *texts: str, ignore_case: bool = True) -> None:
        self.texts = set(t.lower() if ignore_case else t for t in texts)
        self.ignore_case = ignore_case

    async def __call__(self, event: Any) -> bool:
        if not isinstance(event, Message) or not event.text:
            return False
        text = event.text.lower() if self.ignore_case else event.text
        return text in self.texts


class TextContains(Filter):
    """
    Filters messages containing any of the given substrings.
    """
    def __init__(self, *substrings: str, ignore_case: bool = True) -> None:
        self.substrings = [s.lower() if ignore_case else s for s in substrings]
        self.ignore_case = ignore_case

    async def __call__(self, event: Any) -> bool:
        if not isinstance(event, Message) or not event.text:
            return False
        text = event.text.lower() if self.ignore_case else event.text
        return any(sub in text for sub in self.substrings)


class TextStartsWith(Filter):
    """
    Filters messages starting with any of the given prefixes.
    """
    def __init__(self, *prefixes: str, ignore_case: bool = True) -> None:
        self.prefixes = tuple(p.lower() if ignore_case else p for p in prefixes)
        self.ignore_case = ignore_case

    async def __call__(self, event: Any) -> bool:
        if not isinstance(event, Message) or not event.text:
            return False
        text = event.text.lower() if self.ignore_case else event.text
        return text.startswith(self.prefixes)


class TextEndsWith(Filter):
    """
    Filters messages ending with any of the given suffixes.
    """
    def __init__(self, *suffixes: str, ignore_case: bool = True) -> None:
        self.suffixes = tuple(s.lower() if ignore_case else s for s in suffixes)
        self.ignore_case = ignore_case

    async def __call__(self, event: Any) -> bool:
        if not isinstance(event, Message) or not event.text:
            return False
        text = event.text.lower() if self.ignore_case else event.text
        return text.endswith(self.suffixes)
