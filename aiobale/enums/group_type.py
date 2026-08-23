from enum import Enum

class GroupType(int, Enum):
    """
    Enum representing different types of groups.
    """
    
    GROUP = 0
    """Represents a standard group."""

    CHANNEL = 1
    """Represents a channel."""

    SUPERGROUP = 2
    """Represents a supergroup."""
