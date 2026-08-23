from enum import Enum


class GivingType(int, Enum):
    """
    Enumeration for defining how items are given.
    """

    SAME = 0
    """Always give the same item or value each time."""

    RANDOM = 1
    """Give a random item or value each time."""
