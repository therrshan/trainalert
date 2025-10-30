"""Base notifier class."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import io


class BaseNotifier(ABC):
    """Abstract base class for all notifiers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the notifier.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.enabled = True
    
    @abstractmethod
    def send_message(
        self,
        subject: str,
        message: str,
        attachments: Optional[List[io.BytesIO]] = None,
        **kwargs
    ) -> bool:
        """
        Send a notification message.
        
        Args:
            subject: Message subject
            message: Message body
            attachments: Optional list of attachments
            **kwargs: Additional parameters
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    def disable(self):
        """Disable this notifier."""
        self.enabled = False
    
    def enable(self):
        """Enable this notifier."""
        self.enabled = True
    
    def is_enabled(self) -> bool:
        """Check if notifier is enabled."""
        return self.enabled