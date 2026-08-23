from enum import Enum

class SendType(int, Enum):
    """
    Enum representing the types of content that can be sent.
    """
    
    UNKNOWN = 0
    """Represents an unknown send type."""
    
    PHOTO = 1
    """Represents a photo send type."""
    
    VIDEO = 2
    """Represents a video send type."""
    
    VOICE = 3
    """Represents a voice message send type."""
    
    GIF = 4
    """Represents a GIF send type."""
    
    AUDIO = 5
    """Represents an audio file send type."""
    
    DOCUMENT = 6
    """Represents a document send type."""
    
    STICKER = 7
    """Represents a sticker send type."""
    
    CROWDFUNDING = 8
    """Represents a crowdfunding send type."""
