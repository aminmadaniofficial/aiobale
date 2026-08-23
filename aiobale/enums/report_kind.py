from enum import Enum


class ReportKind(int, Enum):
    """
    Enum representing the types of reports that can be submitted.
    """
    
    UNKNOWN = 0
    """Represents an unknown report type."""
    
    SCAM = 1
    """Represents a report for scam-related activities."""
    
    INAPPROPRIATE_CONTENT = 2
    """Represents a report for inappropriate content."""
    
    OTHER = 3
    """Represents a report for other unspecified reasons."""
    
    VIOLENCE = 4
    """Represents a report for violent content or behavior."""
    
    SPAM = 5
    """Represents a report for spam or unsolicited messages."""
    
    FALSE_INFORMATION = 6
    """Represents a report for spreading false information."""
