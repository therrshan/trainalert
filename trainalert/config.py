"""Configuration management for TrainAlert."""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for TrainAlert."""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config_dict: Optional dictionary with configuration values
        """
        self.config = config_dict or {}
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'EMAIL_ADDRESS': 'email_address',
            'EMAIL_PASSWORD': 'email_password',
            'SMTP_SERVER': 'smtp_server',
            'SMTP_PORT': 'smtp_port',
            'SLACK_WEBHOOK_URL': 'slack_webhook_url',
            'DISCORD_WEBHOOK_URL': 'discord_webhook_url',
        }
        
        for env_key, config_key in env_mappings.items():
            value = os.getenv(env_key)
            if value and config_key not in self.config:
                # Convert port to int if applicable
                if config_key == 'smtp_port':
                    value = int(value)
                self.config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
    
    def update(self, config_dict: Dict[str, Any]):
        """Update configuration with dictionary."""
        self.config.update(config_dict)


# Default SMTP configurations for common providers
SMTP_CONFIGS = {
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
    },
    'outlook': {
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587,
    },
    'yahoo': {
        'smtp_server': 'smtp.mail.yahoo.com',
        'smtp_port': 587,
    },
}