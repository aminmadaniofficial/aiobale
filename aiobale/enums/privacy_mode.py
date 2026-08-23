from enum import Enum

class PrivacyMode(int, Enum):
    """
    Enum representing the privacy modes.
    """
    
    UNKNOWN = 0
    """Represents an unknown privacy mode."""
    
    NONE = 1
    """Represents no privacy mode."""
    
    SPAM = 2
    """Represents a spam-related privacy mode."""
