from __future__ import annotations
from typing import Any, Callable, Dict, Generic, List, Optional, Sequence, TypeVar, Union
from .keyboard import InlineKeyboardBuilder, InlineKeyboardButton

T = TypeVar("T")


class KeyboardPaginator(Generic[T]):
    """
    Utility for paginating arbitrary lists into interactive Inline Keyboards.

    Example:
        ```python
        products = ["کتاب پایتون", "کتاب جنگو", "کتاب رست", "کتاب کاتلین", "کتاب گو"]
        paginator = KeyboardPaginator(
            items=products,
            page_size=2,
            item_button_factory=lambda item, idx: InlineKeyboardButton(
                text=item, callback_data=f"prod:{idx}"
            ),
            callback_prefix="page",
        )

        # Get markup for page 1
        markup = paginator.get_page(page=1)
        ```
    """

    def __init__(
        self,
        items: Sequence[T],
        page_size: int = 5,
        item_button_factory: Optional[Callable[[T, int], Union[InlineKeyboardButton, Dict[str, Any]]]] = None,
        callback_prefix: str = "page",
        prev_button_text: str = "◀️ قبلی",
        next_button_text: str = "بعدی ▶️",
        page_indicator_format: str = "📄 {current} / {total}",
    ) -> None:
        self.items: List[T] = list(items)
        self.page_size: int = max(1, page_size)
        self.item_button_factory: Optional[Callable[[T, int], Union[InlineKeyboardButton, Dict[str, Any]]]] = item_button_factory
        self.callback_prefix: str = callback_prefix
        self.prev_button_text: str = prev_button_text
        self.next_button_text: str = next_button_text
        self.page_indicator_format: str = page_indicator_format

    @property
    def total_pages(self) -> int:
        """Total number of pages."""
        if not self.items:
            return 1
        return (len(self.items) + self.page_size - 1) // self.page_size

    def get_page_items(self, page: int) -> List[T]:
        """Returns the slice of items for a given 1-indexed page number."""
        page = max(1, min(page, self.total_pages))
        start_idx = (page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        return self.items[start_idx:end_idx]

    def _format_button(self, btn: Any) -> Dict[str, Any]:
        """Converts any button representation into a valid dictionary for markup."""
        if isinstance(btn, dict):
            return btn
        if hasattr(btn, "model_dump"):
            return btn.model_dump(exclude_none=True)
        return {"text": str(btn)}

    def get_page(self, page: int = 1) -> List[List[Dict[str, Any]]]:
        """Builds and returns the serialized keyboard markup list of rows for the specified page."""
        page = max(1, min(page, self.total_pages))
        rows: List[List[Dict[str, Any]]] = []

        # Render item buttons (1 per row)
        start_idx = (page - 1) * self.page_size
        page_items = self.get_page_items(page)

        for offset, item in enumerate(page_items):
            global_idx = start_idx + offset
            if self.item_button_factory:
                btn = self.item_button_factory(item, global_idx)
            else:
                btn = InlineKeyboardButton(
                    text=str(item),
                    callback_data=f"{self.callback_prefix}:item:{global_idx}",
                )
            rows.append([self._format_button(btn)])

        # Navigation row (if more than 1 page)
        if self.total_pages > 1:
            nav_row: List[Dict[str, Any]] = []

            if page > 1:
                nav_row.append(
                    InlineKeyboardButton(
                        text=self.prev_button_text,
                        callback_data=f"{self.callback_prefix}:{page - 1}",
                    ).model_dump(exclude_none=True)
                )
            else:
                nav_row.append(
                    InlineKeyboardButton(
                        text="⏹️",
                        callback_data=f"{self.callback_prefix}:noop",
                    ).model_dump(exclude_none=True)
                )

            # Page Indicator
            indicator_text = self.page_indicator_format.format(
                current=page, total=self.total_pages
            )
            nav_row.append(
                InlineKeyboardButton(
                    text=indicator_text,
                    callback_data=f"{self.callback_prefix}:current",
                ).model_dump(exclude_none=True)
            )

            if page < self.total_pages:
                nav_row.append(
                    InlineKeyboardButton(
                        text=self.next_button_text,
                        callback_data=f"{self.callback_prefix}:{page + 1}",
                    ).model_dump(exclude_none=True)
                )
            else:
                nav_row.append(
                    InlineKeyboardButton(
                        text="⏹️",
                        callback_data=f"{self.callback_prefix}:noop",
                    ).model_dump(exclude_none=True)
                )

            rows.append(nav_row)

        return rows
