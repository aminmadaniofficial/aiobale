from enum import Enum

class PeerSource(int, Enum):
    """
    Enum representing the source of a peer.
    """
    
    UNKNOWN = 0
    """Represents an unknown source."""
    
    DIALOGS = 1
    """Represents a source from dialogs."""
    
    VITRINE = 2
    """Represents a source from the vitrine."""
    
    MARKET = 3
    """Represents a source from the market."""
    
    PRIVACY_BAR = 4
    """Represents a source from the privacy bar."""
