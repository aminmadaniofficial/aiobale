from enum import Enum

class SendCodeType(int, Enum):
    """
    Enum representing the types of send code methods.
    """
    
    UNKNOWN = 0
    """Represents an unknown send code type."""
    
    DEFAULT = 1
    """Represents the default send code type."""
    
    BALEONLY = 2
    """Represents a send code type specific to Bale only."""
    
    SMS = 3
    """Represents sending the code via SMS."""
    
    CALL = 4
    """Represents sending the code via a phone call."""
    
    EMAIL = 5
    """Represents sending the code via email."""
    
    MISSCALL = 6
    """Represents sending the code via a missed call."""
    
    SETUP_EMAIL_REQUIRED = 7
    """Represents a send code type where email setup is required."""
    
    WHATSAPP = 8
    """Represents sending the code via WhatsApp."""
    
    TELEGRAM = 9
    """Represents sending the code via Telegram."""
    
    USSD = 10
    """Represents sending the code via USSD."""
    
    FUTURE_AUTH_TOKEN = 11
    """Represents a future authentication token send code type."""
    
    TELEGRAM_GATEWAY = 12
    """Represents sending the code via a Telegram gateway."""
