from enum import Enum


class PeerType(int, Enum):
    """
    Enum representing the types of peers in the system.
    """
    
    UNKNOWN = 0
    """Represents an unknown peer type."""
    
    PRIVATE = 1
    """Represents private peers, such as `Users` and `Bots`."""
    
    GROUP = 2
    """Represents group peers, such as `Channels` and `Groups`."""
