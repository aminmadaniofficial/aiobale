from enum import Enum

class ListLoadMode(int, Enum):
    """
    Enum representing the modes for loading a list.
    """
    
    UNKNOWN = 0
    """Represents an unknown load mode."""
    
    FORWARD = 1
    """Represents loading the list in a forward direction."""
    
    BACKWARD = 2
    """Represents loading the list in a backward direction."""
    
    BOTH = 3
    """Represents loading the list in both directions."""
