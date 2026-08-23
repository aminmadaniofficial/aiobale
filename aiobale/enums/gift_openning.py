from enum import Enum


class GiftOpenning(int, Enum):
    """
    Represents the result or status when attempting to open a gift.
    """

    ALREADY_RECEIVED = 0
    """The gift has already been claimed by the user."""

    SOLD_OUT = 1
    """The gift is no longer available."""

    GIFT_CREATOR = 2
    """The current user is the creator of the gift."""

    SUCCESSFUL = 3
    """The gift was successfully opened and received."""

    PENDING = 4
    """The gift opening process is pending or waiting for completion."""
