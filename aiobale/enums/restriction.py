from enum import Enum


class Restriction(int, Enum):
    """
    Enum representing the group visibility levels.
    """
    
    PRIVATE = 0
    """Represents a private group visibility level."""
    
    PUBLIC = 1
    """Represents a public group visibility level."""
