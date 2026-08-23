from enum import Enum


class TypingMode(int, Enum):
    """
    Enum representing the different typing modes.
    """
    
    UNKNOWN = 0
    """Represents an unknown typing mode."""
    
    TEXT = 1
    """Represents typing in text mode."""
    
    VOICERECODRING = 2
    """Represents recording a voice message."""
    
    SENDINGVOICE = 3
    """Represents sending a voice message."""
    
    SENDINGFILE = 4
    """Represents sending a file."""
    
    SENDINGPHOTO = 5
    """Represents sending a photo."""
    
    SENDINGVIDEO = 6
    """Represents sending a video."""
    
    SENDINGMUSIC = 7
    """Represents sending music."""
    
    CHOOSINGSTICKER = 8
    """Represents choosing a sticker."""
    
    CHOSINGGIF = 9
    """Represents choosing a GIF."""
    
    CREATINGGIFTPACKET = 10
    """Represents creating a gift packet."""
    
    SENDINGALBUM = 11
    """Represents sending an album."""
    
    CHOSINGEMOJI = 12
    """Represents choosing an emoji."""
